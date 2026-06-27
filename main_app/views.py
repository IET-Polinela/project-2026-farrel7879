from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Report
from .forms import ReportForm
from .serializers import ReportSerializer


# =========================
# HOME
# =========================
def home(request):

    reports = Report.objects.all()

    context = {
        'total_reports': reports.count(),
        'reported_count': reports.filter(status='REPORTED').count(),
        'verified_count': reports.filter(status='VERIFIED').count(),
        'progress_count': reports.filter(status='IN_PROGRESS').count(),
        'resolved_count': reports.filter(status='RESOLVED').count(),
    }

    return render(request, 'main_app/home.html', context)


# =========================
# REPORT SEARCH
# =========================
def report_search(request):

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthenticated'}, status=403)

    if not request.user.is_admin:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Ambil keyword pencarian dari parameter 'q'
    query = request.GET.get('q', '')
    reports = Report.objects.filter(title__icontains=query)

    # Susun data menjadi bentuk list of dictionaries untuk format JSON
    results = []
    for r in reports:
        results.append({
            'id': r.id,
            'title': r.title,
            'category': r.category,
            # Ambil label display choice jika ada, kalau tidak pakai value aslinya
            'category_display': r.get_category_display() if hasattr(r, 'get_category_display') else r.category,
            'location': r.location,
            'status': r.status if r.status else 'REPORTED',
        })

    # Kembalikan dalam bentuk JsonResponse sesuai ekspektasi Playwright & Frontend JS
    return JsonResponse({'results': results})

# =========================
# REPORT LIST
# =========================
class ReportListView(LoginRequiredMixin, ListView):

    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    paginate_by = 5
    ordering = ['-created_at']

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        queryset = super().get_queryset()

        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

# =========================
# CREATE REPORT
# =========================
class ReportCreateView(LoginRequiredMixin, CreateView):

    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa menambah laporan")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        messages.success(self.request, "Laporan berhasil ditambahkan")

        return super().form_valid(form)

    def form_invalid(self, form):

        print("FORM ERROR =", form.errors)

        return super().form_invalid(form)

# =========================
# DETAIL REPORT
# =========================
class ReportDetailView(LoginRequiredMixin, DetailView):

    model = Report
    template_name = 'main_app/report_detail.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa melihat detail")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

# =========================
# UPDATE REPORT
# =========================
class ReportUpdateView(LoginRequiredMixin, UpdateView):

    model = Report
    form_class = ReportForm
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa update")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        messages.success(self.request, "Laporan berhasil diupdate")

        return super().form_valid(form)

# =========================
# DELETE REPORT
# =========================
class ReportDeleteView(LoginRequiredMixin, DeleteView):

    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa menghapus")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        messages.success(request, "Laporan berhasil dihapus")

        return super().delete(request, *args, **kwargs)


# =========================
# UPDATE STATUS
# =========================
class ReportUpdateStatusView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa update status")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):

        report = get_object_or_404(Report, pk=pk)

        new_status = request.POST.get('status')

        allowed_transitions = {
            'REPORTED': 'VERIFIED',
            'VERIFIED': 'IN_PROGRESS',
            'IN_PROGRESS': 'RESOLVED'
        }

        if report.status in allowed_transitions:

            if allowed_transitions[report.status] == new_status:

                report.status = new_status
                report.save()

                messages.success(request, "Status berhasil diperbarui")

            else:
                messages.error(request, "Transisi status tidak valid")

        return redirect('report_list')


# =========================
# DASHBOARD JSON API
# =========================
def dashboard_data(request):

    status_data = list(
        Report.objects
        .values('status')
        .annotate(total=Count('id'))
    )

    category_data = list(
        Report.objects
        .values('category')
        .annotate(total=Count('id'))
    )

    latest_reported = list(
        Report.objects
        .filter(status='REPORTED')
        .order_by('-created_at')[:5]
        .values('id', 'title', 'location', 'created_at')
    )

    latest_resolved = list(
        Report.objects
        .filter(status='RESOLVED')
        .order_by('-created_at')[:5]
        .values('id', 'title', 'location', 'created_at')
    )

    return JsonResponse({
        'status': status_data,
        'category': category_data,
        'latest_reported': latest_reported,
        'latest_resolved': latest_resolved,
    })


# =========================
# DETAIL API
# =========================
def report_detail_api(request, pk):

    report = get_object_or_404(Report, pk=pk)

    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
        'created_at': report.created_at.strftime("%d %B %Y %H:%M"),
    }

    return JsonResponse(data)


# =========================
# DRF API REPORTS
# =========================
@api_view(['GET'])
def api_reports(request):

    reports = Report.objects.all().order_by('-created_at')

    serializer = ReportSerializer(reports, many=True)

    return Response(serializer.data)
