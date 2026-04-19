from django.urls import path
from .views import (
    home,  # 👈 TAMBAH INI
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
)

urlpatterns = [

    # ✅ HOME (Landing Page)
    path('', home, name='home'),

    # ✅ LIST
    path('reports/', ReportListView.as_view(), name='report_list'),

    # DETAIL
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),

    # CREATE
    path('reports/add/', ReportCreateView.as_view(), name='add_report'),

    # UPDATE
    path('reports/<int:pk>/edit/', ReportUpdateView.as_view(), name='update_report'),

    # DELETE
    path('reports/<int:pk>/delete/', ReportDeleteView.as_view(), name='delete_report'),

    # WORKFLOW
    path('reports/<int:pk>/status/', ReportUpdateStatusView.as_view(), name='update_status'),
]