
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from roles.models import Role, Permission
from employees.models import Employee


class EmployeeSecurityAndRBACTests(APITestCase):

    def setUp(self):
        # Permissions for Employee Management
        self.emp_view = Permission.objects.create(module="Employee Management", action="View")
        self.emp_create = Permission.objects.create(module="Employee Management", action="Create")
        self.emp_edit = Permission.objects.create(module="Employee Management", action="Edit")
        self.emp_delete = Permission.objects.create(module="Employee Management", action="Delete")

        # Roles
        self.admin_role = Role.objects.create(name="Administrator")
        self.admin_role.permissions.add(self.emp_view, self.emp_create, self.emp_edit, self.emp_delete)

        self.hr_manager_role = Role.objects.create(name="HR Manager")
        self.hr_manager_role.permissions.add(self.emp_view, self.emp_create, self.emp_edit, self.emp_delete)

        # HR Executive: View + Create ONLY (No Edit, No Delete)
        self.hr_exec_role = Role.objects.create(name="HR Executive")
        self.hr_exec_role.permissions.add(self.emp_view, self.emp_create)

        self.employee_role = Role.objects.create(name="Employee")

        # Users
        self.admin_user = User.objects.create_user(
            username="admin_emp", email="admin_emp@example.com",
            password="Password123!", role=self.admin_role, is_staff=True, is_superuser=True
        )

        self.hr_manager = User.objects.create_user(
            username="hr_mgr", email="hrmgr@example.com",
            password="Password123!", role=self.hr_manager_role
        )

        self.hr_exec = User.objects.create_user(
            username="hr_exec_user", email="hrexec@example.com",
            password="Password123!", role=self.hr_exec_role
        )

        self.employee_user = User.objects.create_user(
            username="regular_emp", email="regular@example.com",
            password="Password123!", role=self.employee_role
        )

        self.other_employee_user = User.objects.create_user(
            username="other_emp", email="other@example.com",
            password="Password123!", role=self.employee_role
        )

        # Employee profiles
        self.emp_profile_1 = Employee.objects.create(
            user=self.employee_user,
            employee_id="EMP-101",
            department="IT Support",
            designation="Support Specialist",
            phone="111-222-3333",
            address="Private Address 1"
        )

        self.emp_profile_2 = Employee.objects.create(
            user=self.other_employee_user,
            employee_id="EMP-102",
            department="Finance",
            designation="Accountant",
            phone="444-555-6666",
            address="Private Address 2"
        )

    def test_hr_manager_can_view_create_edit_delete_employee(self):
        """Scenario 2: HR Manager can view and manage employee records"""
        self.client.force_authenticate(user=self.hr_manager)

        # View
        view_res = self.client.get("/api/employees/")
        self.assertEqual(view_res.status_code, status.HTTP_200_OK)

        # Create
        create_res = self.client.post("/api/employees/", {
            "username": "new_hire",
            "email": "new_hire@example.com",
            "password": "Password12345!",
            "employee_id": "EMP-103",
            "department": "Engineering",
            "designation": "Developer"
        })
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)

        # Edit
        edit_res = self.client.patch(f"/api/employees/{self.emp_profile_1.id}/", {
            "department": "IT Operations"
        })
        self.assertEqual(edit_res.status_code, status.HTTP_200_OK)

        # Delete
        del_res = self.client.delete(f"/api/employees/{self.emp_profile_1.id}/")
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_hr_executive_can_view_and_create_employees(self):
        """Scenario 4: HR Executive can view and create employee records"""
        self.client.force_authenticate(user=self.hr_exec)

        # View
        view_res = self.client.get("/api/employees/")
        self.assertEqual(view_res.status_code, status.HTTP_200_OK)

        # Create
        create_res = self.client.post("/api/employees/", {
            "username": "exec_created",
            "email": "exec_created@example.com",
            "password": "Password12345!",
            "employee_id": "EMP-104",
            "department": "Sales",
            "designation": "Sales Associate"
        })
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)

    def test_hr_executive_cannot_edit_employee_records(self):
        """Scenario 4: HR Executive cannot edit employee records"""
        self.client.force_authenticate(user=self.hr_exec)
        response = self.client.patch(f"/api/employees/{self.emp_profile_1.id}/", {
            "department": "Unauthorized Edit"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hr_executive_cannot_delete_employee_records(self):
        """Scenario 4: HR Executive cannot delete employee records"""
        self.client.force_authenticate(user=self.hr_exec)
        response = self.client.delete(f"/api/employees/{self.emp_profile_1.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_view_all_employees(self):
        """Scenario 5: Employees cannot view other employees' private information"""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_view_specific_other_employee(self):
        """Scenario 5: Employees cannot view another specific employee record"""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get(f"/api/employees/{self.emp_profile_2.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_view_own_profile(self):
        """Employee access: can access personal dashboard and own profile"""
        self.client.force_authenticate(user=self.employee_user)
        response = self.client.get("/api/employees/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["employee_id"], "EMP-101")
        self.assertEqual(response.data["username"], "regular_emp")
