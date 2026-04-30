from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from main_app.models import Report

class DashboardView(TemplateView):
    template_name = 'dashboard/home.html'


def dashboard_data(request):

    status_data = list(
        Report.objects.values('status').annotate(total=Count('id'))
    )

    category_data = list(
        Report.objects.values('category').annotate(total=Count('id'))
    )

    latest_reported = list(
        Report.objects.filter(status='REPORTED')
        .order_by('-created_at')[:5]
        .values('title', 'location')
    )

    latest_resolved = list(
        Report.objects.filter(status='RESOLVED')
        .order_by('-created_at')[:5]
        .values('title', 'location')
    )

    return JsonResponse({
        'status': status_data,
        'category': category_data,
        'latest_reported': latest_reported,
        'latest_resolved': latest_resolved,
    })