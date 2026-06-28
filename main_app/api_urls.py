from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

router = DefaultRouter(trailing_slash=True)

# 1. Daftarkan versi JAMAK (Untuk kebutuhan Frontend / Playwright)
router.register(
    r"reports",
    ReportViewSet,
    basename="reports",
)

# 2. Daftarkan versi TUNGGAL (Untuk kebutuhan Unit Test Backend Dosen)
router.register(
    r"report",
    ReportViewSet,
    basename="report",
)

urlpatterns = router.urls