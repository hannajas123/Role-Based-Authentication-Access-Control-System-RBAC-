
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    generated_by_username = serializers.CharField(
        source="generated_by.username",
        read_only=True
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "report_type",
            "generated_by_username",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "generated_by_username",
            "created_at",
        ]
