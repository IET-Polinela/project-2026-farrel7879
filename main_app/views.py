from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Report

# LIST (ganti home)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'


# DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# CREATE (ganti add_report)
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')


# UPDATE (ganti update_report)
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')


# DELETE (ganti delete_report)
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')


# WORKFLOW STATUS
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('report_list')