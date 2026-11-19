
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from roles.models import Role
from employees.models import Employee


class EmployeeSecurityTests(TestCase):

    def setUp(self):
        self.employee_role = Role.objects.create(
            name="Employee",
            description="Regular employee"
        )

        self.user = User.objects.create_user(
            username="privacy_test",
            email="privacy@example.com",
            password="TestPassword123",
            role=self.employee_role
        )

        self.other_user = User.objects.create_user(
            username="other_employee",
            email="other@example.com",
            password="TestPassword123",
            role=self.employee_role
        )

        Employee.objects.create(
            user=self.user,
            employee_id="EMP001",
            department="IT",
            designation="Developer"
        )

        Employee.objects.create(
            user=self.other_user,
            employee_id="EMP002",
            department="HR",
            designation="Executive"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_employee_can_view_own_profile(self):
        response = self.client.get("/api/employees/me/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_employee_cannot_view_all_employees(self):
        response = self.client.get("/api/employees/")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_employee_cannot_view_another_employee(self):
        other_employee = Employee.objects.get(
            user=self.other_user
        )

        response = self.client.get(
            f"/api/employees/{other_employee.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
