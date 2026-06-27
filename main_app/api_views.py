from django.db.models import Q

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Report
from .permissions import IsOwnerAndDraftOrReadOnly
from .serializers import ReportSerializer


# ==========================================================
# PAGINATION
# ==========================================================
class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


# ==========================================================
# PERMISSION CITIZEN
# ==========================================================
class IsCitizen(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.is_admin
        )


# ==========================================================
# REPORT VIEWSET
# ==========================================================
class ReportViewSet(viewsets.ModelViewSet):

    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    # ------------------------------------------------------
    # QUERYSET
    # ------------------------------------------------------
    def get_queryset(self):

        user = self.request.user

        if not user.is_authenticated:
            return Report.objects.none()

        queryset = Report.objects.select_related(
            "reporter"
        ).order_by("-updated_at")

        tab = self.request.query_params.get("tab")

        # ======================
        # MY REPORTS
        # ======================
        if tab == "my_reports":
            return queryset.filter(reporter=user)

        # ======================
        # FEED KOTA
        # ======================
        if tab == "feed":
            return queryset.exclude(
                status="DRAFT"
            )

        # ======================
        # DEFAULT
        # ======================
        return queryset.filter(
            Q(reporter=user) |
            ~Q(status="DRAFT")
        )

    # ------------------------------------------------------
    # PERMISSIONS
    # ------------------------------------------------------
    def get_permissions(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [
                permissions.IsAuthenticated
            ]

        elif self.action == "create":
            permission_classes = [
                permissions.IsAuthenticated,
                IsCitizen,
            ]

        elif self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerAndDraftOrReadOnly,
            ]

        elif self.action == "update_status":
            permission_classes = [
                permissions.IsAdminUser,
            ]

        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    # ------------------------------------------------------
    # SERIALIZER CONTEXT
    # ------------------------------------------------------
    def get_serializer_context(self):

        context = super().get_serializer_context()

        context["request"] = self.request

        return context

    # ------------------------------------------------------
    # CREATE
    # ------------------------------------------------------
    def perform_create(self, serializer):

        requested_status = self.request.data.get(
            "status",
            "DRAFT"
        )

        if requested_status not in [
            "DRAFT",
            "REPORTED",
        ]:
            requested_status = "DRAFT"

        serializer.save(
            reporter=self.request.user,
            status=requested_status,
        )

    # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------
    def perform_update(self, serializer):

        report = self.get_object()

        requested_status = self.request.data.get(
            "status",
            report.status,
        )

        if report.status == "DRAFT":

            if requested_status in [
                "DRAFT",
                "REPORTED",
            ]:
                serializer.save(
                    status=requested_status
                )
                return

        serializer.save()

    # ------------------------------------------------------
    # UPDATE STATUS (ADMIN)
    # ------------------------------------------------------
    @extend_schema(exclude=True)
    @action(
        detail=True,
        methods=["patch"],
        url_path="update-status",
    )
    def update_status(self, request, pk=None):

        report = self.get_object()

        new_status = request.data.get("status")

        allowed_status = [
            "REPORTED",
            "VERIFIED",
            "IN_PROGRESS",
            "RESOLVED",
        ]

        if new_status not in allowed_status:

            return Response(
                {
                    "detail": "Status tidak valid."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        report.status = new_status

        report.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        serializer = self.get_serializer(report)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )