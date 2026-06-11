from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    register_api,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    # API REGISTER
    path("api/register/", register_api, name="api_register"),
]