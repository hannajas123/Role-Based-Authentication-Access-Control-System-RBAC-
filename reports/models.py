
from django.conf import settings
from django.db import models


class Report(models.Model):
    REPORT_TYPES = [
        ("employee", "Employee Report"),
        ("financial", "Financial Report"),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPES
    )
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="generated_reports"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
