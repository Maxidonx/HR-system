from django.urls import path
from .views import ReportingDashboardView, EmployeeReportExportView

urlpatterns = [
    path('dashboard-summary/', ReportingDashboardView.as_view(), name='report-dashboard-summary'),
    path('export/employees/', EmployeeReportExportView.as_view(), name='report-export-employees'),
]
