from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from .models import Report
from .forms import ReportForm


class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get('q')
        status = self.request.GET.get('status')

        if q:
            qs = qs.filter(title__icontains=q)

        if status:
            qs = qs.filter(status=status)

        return qs


class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan")
        return super().form_valid(form)


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate")
        return super().form_valid(form)


class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus")
        return super().delete(request, *args, **kwargs)


class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)

        new_status = request.POST.get('status')

        # aturan workflow sesuai lab 5
        allowed_transitions = {
            'REPORTED': 'VERIFIED',
            'VERIFIED': 'IN_PROGRESS',
            'IN_PROGRESS': 'RESOLVED'
        }

        # validasi biar gak loncat status
        if report.status in allowed_transitions:
            if allowed_transitions[report.status] == new_status:
                report.status = new_status
                report.save()

        return redirect('report_list')


def home(request):
    reports = Report.objects.all()

    context = {
        'total_reports': reports.count(),
        'reported_count': reports.filter(status='REPORTED').count(),
        'verified_count': reports.filter(status='VERIFIED').count(),  # 🔥 TAMBAH INI
        'progress_count': reports.filter(status='IN_PROGRESS').count(),
        'resolved_count': reports.filter(status='RESOLVED').count(),
    }

    return render(request, 'main_app/home.html', context)