from rest_framework.routers import DefaultRouter

from .api_views import ReportViewSet


router = DefaultRouter(trailing_slash=True)

router.register(
    r"reports",
    ReportViewSet,
    basename="reports",
)

urlpatterns = router.urls