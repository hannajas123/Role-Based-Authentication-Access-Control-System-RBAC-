
from django.core.management.base import BaseCommand
from roles.models import Role, Permission


class Command(BaseCommand):
    help = "Create predefined RBAC roles and permissions"

    def handle(self, *args, **kwargs):

        # All available module/action combinations
        permission_data = {
            "Dashboard": ["View"],

            "User Management": [
                "View", "Create", "Edit", "Delete"
            ],

            "Role Management": [
                "View", "Create", "Edit", "Delete"
            ],

            "Employee Management": [
                "View", "Create", "Edit", "Delete"
            ],

            "Reports": [
                "View", "Generate", "Download"
            ],

            "Settings": ["View", "Edit"],
        }

        # Create permissions in the database
        permission_objects = {}

        for module, actions in permission_data.items():
            for action in actions:
                permission, created = Permission.objects.get_or_create(
                    module=module,
                    action=action
                )

                permission_objects[(module, action)] = permission

        # Define the permissions assigned to each role
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
            "Administrator": "Full access to all application modules.",
            "HR Manager": "Manages employee records and HR reports.",
            "HR Executive": "Can view and create employee records.",
            "Finance Manager": "Access to dashboard and financial reports.",
            "Employee": "Access to personal dashboard and own information.",
        }

        # Create roles and assign their permissions
        for role_name, permissions in role_permissions.items():

            role, created = Role.objects.get_or_create(
                name=role_name,
                defaults={
                    "description": descriptions[role_name]
                }
            )

            # Keep description updated
            role.description = descriptions[role_name]
            role.save()

            # Assign the exact permission set
            selected_permissions = [
                permission_objects[item]
                for item in permissions
            ]

            role.permissions.set(selected_permissions)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Role ready: {role_name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "All five RBAC roles and permissions are ready!"
            )
        )
