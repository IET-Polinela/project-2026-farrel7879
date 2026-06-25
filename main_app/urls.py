from django.urls import path

from .views import (
    home,
    report_search,
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    dashboard_data,
    report_detail_api,
)

urlpatterns = [

    # HOME
    path('', home, name='home'),

    # REPORT CRUD
    path(
        'reports/',
        ReportListView.as_view(),
        name='report_list'
    ),

    path(
        'reports/search/',
        report_search,
        name='report_search'
    ),

    path(
        'reports/add/',
        ReportCreateView.as_view(),
        name='add_report'
    ),

    path(
        'reports/<int:pk>/',
        ReportDetailView.as_view(),
        name='report_detail'
    ),

    path(
        'reports/<int:pk>/edit/',
        ReportUpdateView.as_view(),
        name='update_report'
    ),

    path(
        'reports/<int:pk>/delete/',
        ReportDeleteView.as_view(),
        name='delete_report'
    ),

    path(
        'reports/<int:pk>/status/',
        ReportUpdateStatusView.as_view(),
        name='update_status'
    ),

    # DASHBOARD API
    path(
        'dashboard/data/',
        dashboard_data,
        name='dashboard_data'
    ),

    # DETAIL API
    path(
        'api/report-detail/<int:pk>/',
        report_detail_api,
        name='report_api'
    ),

]
