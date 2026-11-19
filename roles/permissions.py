
from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasModulePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        module = getattr(view, "required_module", None)
        if not module:
            return False

        # A view can explicitly require Generate or Download.
        action = getattr(view, "required_action", None)

        if not action:
            if request.method in SAFE_METHODS:
                action = "View"
            elif request.method == "POST":
                action = "Create"
            elif request.method in ["PUT", "PATCH"]:
                action = "Edit"
            elif request.method == "DELETE":
                action = "Delete"
            else:
                return False

        if not user.role:
            return False

        return user.role.permissions.filter(
            module=module,
            action=action
        ).exists()
