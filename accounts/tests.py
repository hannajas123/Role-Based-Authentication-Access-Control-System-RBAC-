
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from roles.models import Role, Permission


class AuthenticationAndUserSecurityTests(APITestCase):

    def setUp(self):
        # Create permissions and roles
        self.dashboard_perm = Permission.objects.create(module="Dashboard", action="View")
        self.user_view_perm = Permission.objects.create(module="User Management", action="View")
        self.user_create_perm = Permission.objects.create(module="User Management", action="Create")

        self.admin_role = Role.objects.create(name="Administrator")
        self.admin_role.permissions.add(self.dashboard_perm, self.user_view_perm, self.user_create_perm)

        self.employee_role = Role.objects.create(name="Employee")
        self.employee_role.permissions.add(self.dashboard_perm)

        # Create Admin
        self.admin_user = User.objects.create_user(
            username="admin_test",
            email="admin_test@example.com",
            password="AdminPassword123!",
            role=self.admin_role,
            is_staff=True,
            is_superuser=True
        )

        # Create Normal Employee
        self.employee_user = User.objects.create_user(
            username="emp_test",
            email="emp_test@example.com",
            password="EmpPassword123!",
            role=self.employee_role
        )

        # Create Deactivated User
        self.inactive_user = User.objects.create_user(
            username="inactive_test",
            email="inactive_test@example.com",
            password="InactivePassword123!",
            role=self.employee_role,
            is_active=False
        )

    def test_login_with_username_success(self):
        """Authentication: login using username"""
        response = self.client.post("/api/auth/login/", {
            "username_or_email": "admin_test",
            "password": "AdminPassword123!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["role"], "Administrator")

    def test_login_with_email_success(self):
        """Authentication: login using email"""
        response = self.client.post("/api/auth/login/", {
            "username_or_email": "emp_test@example.com",
            "password": "EmpPassword123!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "emp_test")

    def test_login_with_invalid_credentials_fails(self):
        """Authentication: invalid password rejected"""
        response = self.client.post("/api/auth/login/", {
            "username_or_email": "emp_test",
            "password": "WrongPassword!"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deactivated_user_cannot_login(self):
        """Scenario 9: Deactivated users cannot access the application"""
        response = self.client.post("/api/auth/login/", {
            "username_or_email": "inactive_test",
            "password": "InactivePassword123!"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_blacklists_refresh_token(self):
        """Authentication: logout blacklists refresh token"""
        login_res = self.client.post("/api/auth/login/", {
            "username_or_email": "emp_test",
            "password": "EmpPassword123!"
        })
        access = login_res.data["access"]
        refresh = login_res.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        logout_res = self.client.post("/api/auth/logout/", {"refresh": refresh})
        self.assertEqual(logout_res.status_code, status.HTTP_205_RESET_CONTENT)

    def test_admin_can_create_user_and_assign_role(self):
        """Scenario 6: Administrator can create users and assign roles"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/auth/users/", {
            "username": "new_created_user",
            "email": "new_user@example.com",
            "password": "NewUserPassword123!",
            "role_id": self.employee_role.id,
            "is_active": True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "new_created_user")
        self.assertEqual(response.data["role_name"], "Employee")

    def test_admin_can_activate_and_deactivate_user(self):
        """User Management: Administrator can deactivate user"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(f"/api/auth/users/{self.employee_user.id}/", {
            "is_active": False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee_user.refresh_from_db()
        self.assertFalse(self.employee_user.is_active)

    def test_non_admin_cannot_access_user_management(self):
        """Scenario 3: Users cannot access unauthorized APIs"""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get("/api/auth/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_elevate_own_role(self):
        """Scenario 10: Users cannot increase their own permissions or privileges"""
        self.client.force_authenticate(user=self.employee_user)
        # Attempt to modify self directly via user endpoint
        response = self.client.patch(f"/api/auth/users/{self.employee_user.id}/", {
            "role_id": self.admin_role.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
