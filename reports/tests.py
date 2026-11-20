
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from roles.models import Role, Permission
from reports.models import Report


class ReportsSecurityAndRBACTests(APITestCase):

    def setUp(self):
        # Report permissions
        self.rep_view = Permission.objects.create(module="Reports", action="View")
        self.rep_gen = Permission.objects.create(module="Reports", action="Generate")
        self.rep_down = Permission.objects.create(module="Reports", action="Download")

        # Roles
        self.admin_role = Role.objects.create(name="Administrator")
        self.admin_role.permissions.add(self.rep_view, self.rep_gen, self.rep_down)

        self.hr_manager_role = Role.objects.create(name="HR Manager")
        self.hr_manager_role.permissions.add(self.rep_view, self.rep_gen, self.rep_down)

        self.finance_manager_role = Role.objects.create(name="Finance Manager")
        self.finance_manager_role.permissions.add(self.rep_view, self.rep_gen, self.rep_down)

        self.employee_role = Role.objects.create(name="Employee")

        # Users
        self.admin_user = User.objects.create_user(
            username="admin_rep", email="admin_rep@example.com",
            password="Password123!", role=self.admin_role, is_staff=True, is_superuser=True
        )

        self.hr_manager = User.objects.create_user(
            username="hr_rep_user", email="hr_rep@example.com",
            password="Password123!", role=self.hr_manager_role
        )

        self.finance_manager = User.objects.create_user(
            username="fin_rep_user", email="fin_rep@example.com",
            password="Password123!", role=self.finance_manager_role
        )

        self.employee_user = User.objects.create_user(
            username="emp_rep_user", email="emp_rep@example.com",
            password="Password123!", role=self.employee_role
        )

        # Pre-existing reports
        self.emp_report = Report.objects.create(
            title="HR Annual Headcount",
            report_type="employee",
            generated_by=self.admin_user
        )

        self.fin_report = Report.objects.create(
            title="Q4 Balance Sheet",
            report_type="financial",
            generated_by=self.admin_user
        )

    def test_admin_can_access_both_report_types(self):
        """Scenario 1: Administrator can access all modules and report types"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/reports/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Both reports visible
        report_ids = [r["id"] for r in response.data]
        self.assertIn(self.emp_report.id, report_ids)
        self.assertIn(self.fin_report.id, report_ids)

    def test_hr_manager_can_access_only_employee_reports(self):
        """Role Access: HR Manager can view and generate only employee reports"""
        self.client.force_authenticate(user=self.hr_manager)

        # List should only include employee report
        list_res = self.client.get("/api/reports/")
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        for r in list_res.data:
            self.assertEqual(r["report_type"], "employee")

        # Generate employee report succeeds
        gen_res = self.client.post("/api/reports/generate/", {
            "title": "New HR Retention Report",
            "report_type": "employee"
        })
        self.assertEqual(gen_res.status_code, status.HTTP_201_CREATED)

        # Generating financial report is forbidden
        gen_fin = self.client.post("/api/reports/generate/", {
            "title": "Attempted Finance Report",
            "report_type": "financial"
        })
        self.assertEqual(gen_fin.status_code, status.HTTP_403_FORBIDDEN)

    def test_finance_manager_can_access_only_financial_reports(self):
        """Role Access: Finance Manager can view and generate only financial reports"""
        self.client.force_authenticate(user=self.finance_manager)

        # List should only include financial report
        list_res = self.client.get("/api/reports/")
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        for r in list_res.data:
            self.assertEqual(r["report_type"], "financial")

        # Generate financial report succeeds
        gen_res = self.client.post("/api/reports/generate/", {
            "title": "New Financial Audit",
            "report_type": "financial"
        })
        self.assertEqual(gen_res.status_code, status.HTTP_201_CREATED)

        # Generating employee report is forbidden
        gen_emp = self.client.post("/api/reports/generate/", {
            "title": "Attempted HR Report",
            "report_type": "employee"
        })
        self.assertEqual(gen_emp.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_access_reports_api(self):
        """Scenario 3: Users without permission cannot access reports"""
        self.client.force_authenticate(user=self.employee_user)
        list_res = self.client.get("/api/reports/")
        self.assertEqual(list_res.status_code, status.HTTP_403_FORBIDDEN)

        gen_res = self.client.post("/api/reports/generate/", {
            "title": "Unauthorized Report",
            "report_type": "employee"
        })
        self.assertEqual(gen_res.status_code, status.HTTP_403_FORBIDDEN)
