from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly


class IsCitizen(permissions.BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and not request.user.is_admin
        )


class ReportViewSet(viewsets.ModelViewSet):

    serializer_class = ReportSerializer

    def get_queryset(self):

        user = self.request.user

        if not user.is_authenticated:
            return Report.objects.none()

        if user.is_admin:
            return Report.objects.exclude(status='DRAFT').order_by('-created_at')

        return Report.objects.filter(
            reporter=user
        ) | Report.objects.exclude(status='DRAFT')

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            return [
                permissions.IsAuthenticated()
            ]

        if self.action == 'create':
            return [
                permissions.IsAuthenticated(),
                IsCitizen()
            ]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [
                permissions.IsAuthenticated(),
                IsOwnerAndDraftOrReadOnly()
            ]

        if self.action == 'update_status':
            return [
                permissions.IsAuthenticated(),
                permissions.IsAdminUser()
            ]

        return [
            permissions.IsAuthenticated()
        ]

    def perform_create(self, serializer):

        serializer.save(
            reporter=self.request.user,
            status='DRAFT'
        )

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):

        report = self.get_object()
        new_status = request.data.get('status')

        allowed_status = [
            'VERIFIED',
            'IN_PROGRESS',
            'RESOLVED'
        ]

        if new_status not in allowed_status:
            return Response(
                {
                    'detail': 'Status tidak valid.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        report.status = new_status
        report.save()

        serializer = self.get_serializer(report)

        return Response(serializer.data)