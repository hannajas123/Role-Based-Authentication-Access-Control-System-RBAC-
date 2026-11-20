
from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from roles.models import Role, Permission
from employees.models import Employee
from reports.models import Report

User = get_user_model()


class Command(BaseCommand):
    help = "Create predefined RBAC roles, permissions, mandatory demo users, and test data"

    def handle(self, *args, **kwargs):
        # 1. Predefined permissions per module
        permission_data = {
            "Dashboard": ["View"],
            "User Management": ["View", "Create", "Edit", "Delete"],
            "Role Management": ["View", "Create", "Edit", "Delete"],
            "Employee Management": ["View", "Create", "Edit", "Delete"],
            "Reports": ["View", "Generate", "Download"],
            "Settings": ["View", "Edit"],
        }

        permission_objects = {}
        for module, actions in permission_data.items():
            for action in actions:
                permission, _ = Permission.objects.get_or_create(
                    module=module,
                    action=action
                )
                permission_objects[(module, action)] = permission

        # 2. Permissions assigned to each role
        role_permissions = {
            "Administrator": [
                (module, action)
                for module, actions in permission_data.items()
                for action in actions
            ],
            "HR Manager": [
                ("Dashboard", "View"),
                ("Employee Management", "View"),
                ("Employee Management", "Create"),
                ("Employee Management", "Edit"),
                ("Employee Management", "Delete"),
                ("Reports", "View"),
                ("Reports", "Generate"),
                ("Reports", "Download"),
            ],
            "HR Executive": [
                ("Dashboard", "View"),
                ("Employee Management", "View"),
                ("Employee Management", "Create"),
            ],
            "Finance Manager": [
                ("Dashboard", "View"),
                ("Reports", "View"),
                ("Reports", "Generate"),
                ("Reports", "Download"),
            ],
            "Employee": [
                ("Dashboard", "View"),
            ],
        }

        descriptions = {
            "Administrator": "Full access to all application modules and configurations.",
            "HR Manager": "Manages employee records and HR reports.",
            "HR Executive": "Can view and create employee records.",
            "Finance Manager": "Access to dashboard and financial reports.",
            "Employee": "Access to personal dashboard and own profile.",
        }

        created_roles = {}
        for role_name, permissions in role_permissions.items():
            role, _ = Role.objects.get_or_create(
                name=role_name,
                defaults={"description": descriptions[role_name]}
            )
            role.description = descriptions[role_name]
            role.save()

            selected_permissions = [
                permission_objects[item] for item in permissions
            ]
            role.permissions.set(selected_permissions)
            created_roles[role_name] = role
            self.stdout.write(self.style.SUCCESS(f"Role ready: {role_name}"))

        # 3. Create/update the 5 Mandatory Test Users
        demo_users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "Admin@12345",
                "role": "Administrator",
                "is_staff": True,
                "is_superuser": True,
                "emp_id": "EMP-001",
                "dept": "Executive",
                "desig": "System Administrator",
            },
            {
                "username": "hr_manager",
                "email": "hrmanager@example.com",
                "password": "HRManager@12345",
                "role": "HR Manager",
                "is_staff": False,
                "is_superuser": False,
                "emp_id": "EMP-002",
                "dept": "Human Resources",
                "desig": "HR Manager",
            },
            {
                "username": "hr_exec",
                "email": "hrexec@example.com",
                "password": "HRExec@12345",
                "role": "HR Executive",
                "is_staff": False,
                "is_superuser": False,
                "emp_id": "EMP-003",
                "dept": "Human Resources",
                "desig": "HR Executive",
            },
            {
                "username": "finance_mgr",
                "email": "finance@example.com",
                "password": "Finance@12345",
                "role": "Finance Manager",
                "is_staff": False,
                "is_superuser": False,
                "emp_id": "EMP-004",
                "dept": "Finance",
                "desig": "Finance Manager",
            },
            {
                "username": "employee_user",
                "email": "employee@example.com",
                "password": "Employee@12345",
                "role": "Employee",
                "is_staff": False,
                "is_superuser": False,
                "emp_id": "EMP-005",
                "dept": "Engineering",
                "desig": "Software Engineer",
            },
        ]

        self.stdout.write("\nProvisioning Mandatory Test Users...")
        for udata in demo_users:
            user, created = User.objects.get_or_create(
                username=udata["username"],
                defaults={
                    "email": udata["email"],
                    "is_active": True,
                    "is_staff": udata["is_staff"],
                    "is_superuser": udata["is_superuser"],
                }
            )
            user.email = udata["email"]
            user.role = created_roles[udata["role"]]
            user.is_active = True
            user.is_staff = udata["is_staff"]
            user.is_superuser = udata["is_superuser"]
            user.set_password(udata["password"])
            user.save()

            # Ensure Employee profile exists
            Employee.objects.update_or_create(
                user=user,
                defaults={
                    "employee_id": udata["emp_id"],
                    "department": udata["dept"],
                    "designation": udata["desig"],
                    "phone": "+1-555-0100",
                    "address": "HQ Office Suite 400",
                    "date_of_joining": date(2025, 1, 15),
                }
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"User ready: {user.username} ({udata['role']}) -> {udata['email']}"
                )
            )

        # 4. Create sample initial reports for testing
        admin_user = User.objects.get(username="admin")
        Report.objects.get_or_create(
            title="Q4 2026 Headcount & Retention Report",
            report_type="employee",
            defaults={"generated_by": admin_user}
        )
        Report.objects.get_or_create(
            title="Q4 2026 Fiscal Financial Statement",
            report_type="financial",
            defaults={"generated_by": admin_user}
        )

        self.stdout.write(self.style.SUCCESS("\nAll RBAC roles, permissions, users, and sample data are ready!\n"))
