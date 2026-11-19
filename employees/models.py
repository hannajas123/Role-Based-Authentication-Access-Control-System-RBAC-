from django.db import models
from django.conf import settings

# Create your models here.

class Employee(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile"
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100)

    phone = models.CharField(max_length=15, blank=True)

    address = models.TextField(blank=True)

    date_of_joining = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.username}"
