
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from roles.models import Role


class RBACTests(APITestCase):

    def setUp(self):
        self.employee_role = Role.objects.create(
            name="Employee",
            description="Regular employee"
        )

        self.employee = User.objects.create_user(
            username="rbac_test_employee",
            email="rbac_test@example.com",
            password="TestPassword123",
            role=self.employee_role
        )

    def test_employee_cannot_access_role_management(self):
        self.client.force_authenticate(user=self.employee)

        response = self.client.get("/api/roles/roles/")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_employee_cannot_access_user_management(self):
        self.client.force_authenticate(user=self.employee)

        response = self.client.get("/api/auth/users/")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
