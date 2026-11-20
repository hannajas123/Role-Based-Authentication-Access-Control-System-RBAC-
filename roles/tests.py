
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from roles.models import Role, Permission


class RoleAndPermissionTests(APITestCase):

    def setUp(self):
        self.dashboard_view = Permission.objects.create(module="Dashboard", action="View")
        self.role_view = Permission.objects.create(module="Role Management", action="View")
        self.role_create = Permission.objects.create(module="Role Management", action="Create")
        self.emp_view = Permission.objects.create(module="Employee Management", action="View")

        self.admin_role = Role.objects.create(name="Administrator")
        self.admin_role.permissions.add(self.dashboard_view, self.role_view, self.role_create, self.emp_view)

        self.employee_role = Role.objects.create(name="Employee")
        self.employee_role.permissions.add(self.dashboard_view)

        self.admin_user = User.objects.create_user(
            username="admin_role_test",
            email="admin_role@example.com",
            password="TestPassword123!",
            role=self.admin_role,
            is_staff=True,
            is_superuser=True
        )

        self.employee_user = User.objects.create_user(
            username="emp_role_test",
            email="emp_role@example.com",
            password="TestPassword123!",
            role=self.employee_role
        )

    def test_admin_can_access_role_management(self):
        """Scenario 1: Administrator can access all modules (Role Management)"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/roles/roles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)

    def test_admin_can_create_role_and_assign_permissions(self):
        """Scenario 7: Administrator can create roles and assign permissions"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/roles/roles/", {
            "name": "Custom Auditor",
            "description": "Audits modules",
            "permission_ids": [self.dashboard_view.id, self.emp_view.id]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Custom Auditor")
        self.assertEqual(len(response.data["permissions"]), 2)

    def test_administrator_role_cannot_be_deleted_or_edited(self):
        """Security: The Administrator role is protected"""
        self.client.force_authenticate(user=self.admin_user)
        # Attempt edit
        edit_res = self.client.patch(f"/api/roles/roles/{self.admin_role.id}/", {
            "description": "Attempt modify"
        })
        self.assertEqual(edit_res.status_code, status.HTTP_403_FORBIDDEN)

        # Attempt delete
        del_res = self.client.delete(f"/api/roles/roles/{self.admin_role.id}/")
        self.assertEqual(del_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_access_roles_api(self):
        """Scenario 3: Users cannot access unauthorized pages or APIs"""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get("/api/roles/roles/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_list_endpoint_accessible(self):
        """Permission Management: Endpoint returns all permissions"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/roles/permissions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 4)

    def test_changes_in_role_permissions_reflected_immediately(self):
        """Scenario 8: Changes in roles and permissions are reflected in user access"""
        self.client.force_authenticate(user=self.employee_user)
        
        # Initially employee cannot access employee-permission-test
        initial_check = self.client.get("/api/roles/employee-permission-test/")
        self.assertEqual(initial_check.status_code, status.HTTP_403_FORBIDDEN)

        # Admin assigns Employee Management View permission to Employee role
        self.employee_role.permissions.add(self.emp_view)

        # User tries again: now granted immediately!
        updated_check = self.client.get("/api/roles/employee-permission-test/")
        self.assertEqual(updated_check.status_code, status.HTTP_200_OK)
