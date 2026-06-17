"""
URL configuration for smartcity_app project.
"""

from django.contrib import admin
from django.urls import include, path

from django_scalar import views as scalar_views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Main App
    path("", include("main_app.urls")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # DRF API
    path("api/", include("main_app.api_urls")),

    # JWT Token
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # OpenAPI Schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger UI
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # Scalar UI
    path(
    "api/docs/scalar/",
    scalar_views.scalar_viewer,
    name="scalar-ui",
    ),
    
    # Other Apps
    path("about/", include("about.urls")),
    path("contacts/", include("contacts.urls")),

    # Authentication
    path(
        "auth/",
        include("usermanagement_24782080.urls"),
    ),
]