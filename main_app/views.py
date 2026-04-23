from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Report
from .forms import ReportForm


# =========================
# HOME (PUBLIC)
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
# LIST (LOGIN REQUIRED)
# =========================
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    paginate_by = 5


# =========================
# CREATE (ADMIN ONLY)
# =========================
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa menambah laporan")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan")
        return super().form_valid(form)


# =========================
# DETAIL
# =========================
class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# =========================
# UPDATE (ADMIN ONLY)
# =========================
class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa update")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate")
        return super().form_valid(form)


# =========================
# DELETE (ADMIN ONLY)
# =========================
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang bisa menghapus")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus")
        return super().delete(request, *args, **kwargs)


# =========================
# UPDATE STATUS (ADMIN ONLY)
# =========================
class ReportUpdateStatusView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
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