from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

# 🔥 PENTING: pakai custom form
from .forms import CustomUserCreationForm


# =========================
# REGISTER (CITIZEN)
# =========================
class RegisterView(CreateView):
    form_class = CustomUserCreationForm   # ✅ FIX
    template_name = 'main_app/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # 🔥 kalau sudah login → gak boleh ke register
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)

        # 🔥 SET ROLE
        user.is_admin = False
        user.is_member = True

        user.save()

        messages.success(self.request, "Registrasi berhasil, silakan login")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registrasi gagal, periksa kembali input")
        return super().form_invalid(form)


# =========================
# LOGIN (CBV)
# =========================
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        # 🔥 kalau sudah login → langsung ke home
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Login berhasil")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Username atau password salah")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')


# =========================
# LOGOUT (CBV)
# =========================
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Logout berhasil")
        return super().dispatch(request, *args, **kwargs)
    
@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    User = get_user_model()

    username = request.data.get("username")
    email = request.data.get("email", "")
    password = request.data.get("password")
    password2 = request.data.get("password2")

    if not username or not password or not password2:
        return Response(
            {"detail": "Username dan password wajib diisi."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if password != password2:
        return Response(
            {"detail": "Konfirmasi password tidak sama."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Username sudah digunakan."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    user.is_admin = False
    user.is_member = True
    user.save()

    return Response(
        {"detail": "Akun berhasil dibuat."},
        status=status.HTTP_201_CREATED
    )