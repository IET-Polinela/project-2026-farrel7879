from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .forms import CustomUserCreationForm


# =========================
# REGISTER BERBASIS TEMPLATE
# =========================
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "main_app/register.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        # User yang sudah login tidak perlu membuka halaman register
        if request.user.is_authenticated:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)

        # Akun baru otomatis menjadi citizen/member
        user.is_admin = False
        user.is_member = True
        user.save()

        messages.success(
            self.request,
            "Registrasi berhasil, silakan login.",
        )

        # Hindari menyimpan user dua kali lewat form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Registrasi gagal, periksa kembali input.",
        )
        return super().form_invalid(form)


# =========================
# LOGIN BERBASIS TEMPLATE
# =========================
class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Login berhasil.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Username atau password salah.",
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("home")


# =========================
# LOGOUT BERBASIS TEMPLATE
# =========================
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Logout berhasil.")
        return super().dispatch(request, *args, **kwargs)


# =========================
# REGISTER API UNTUK SPA
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    User = get_user_model()

    username = str(request.data.get("username", "")).strip()
    email = str(request.data.get("email", "")).strip()
    password = request.data.get("password", "")
    password2 = request.data.get("password2", "")

    if not username or not password or not password2:
        return Response(
            {
                "detail": (
                    "Username, password, dan konfirmasi password "
                    "wajib diisi."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if password != password2:
        return Response(
            {"detail": "Konfirmasi password tidak sama."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Username sudah digunakan."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if email and User.objects.filter(email=email).exists():
        return Response(
            {"detail": "Email sudah digunakan."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    user.is_admin = False
    user.is_member = True
    user.save(update_fields=["is_admin", "is_member"])

    return Response(
        {
            "detail": "Akun berhasil dibuat.",
            "username": user.username,
        },
        status=status.HTTP_201_CREATED,
    )