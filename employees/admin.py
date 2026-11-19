

from django.contrib import admin
from .models import Employee
# Register your models here.


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "user",
        "department",
        "designation",
    )

    search_fields = (
        "employee_id",
        "user__username",
        "department",
    )
