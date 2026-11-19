
from django.urls import path

from .views import (
    ReportListView,
    GenerateReportView,
    DownloadReportView,
)

urlpatterns = [
    path("", ReportListView.as_view(), name="report-list"),
    path("generate/", GenerateReportView.as_view(), name="report-generate"),
    path("<int:pk>/download/", DownloadReportView.as_view(), name="report-download"),
]
