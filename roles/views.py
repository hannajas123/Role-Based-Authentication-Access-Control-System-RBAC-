

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import HasModulePermission

# Create your views here.

class EmployeePermissionTestView(APIView):
    permission_classes = [IsAuthenticated, HasModulePermission]

    required_module = "Employee Management"

    def get(self, request):
        return Response({
            "message": "You can view employee records."
        })

    def post(self, request):
        return Response({
            "message": "You can create employee records."
        })

    def put(self, request):
        return Response({
            "message": "You can edit employee records."
        })

    def delete(self, request):
        return Response({
            "message": "You can delete employee records."
        })



from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Role, Permission
from .serializers import RoleSerializer, PermissionSerializer


class PermissionListView(ListAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all().order_by("module", "action")


class RoleListCreateView(ListCreateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def check_admin(self):
        user = self.request.user
        if not (
            user.is_superuser
            or (
                user.role is not None
                and user.role.name == "Administrator"
            )
        ):
            raise PermissionDenied("Administrator access required.")

    def get_queryset(self):
        self.check_admin()
        return Role.objects.prefetch_related("permissions").all()

    def perform_create(self, serializer):
        self.check_admin()
        serializer.save()


class RoleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def check_admin(self):
        user = self.request.user
        if not (
            user.is_superuser
            or (
                user.role is not None
                and user.role.name == "Administrator"
            )
        ):
            raise PermissionDenied("Administrator access required.")

    def get_queryset(self):
        self.check_admin()
        return Role.objects.prefetch_related("permissions").all()

    def perform_update(self, serializer):
        self.check_admin()

        if serializer.instance.name == "Administrator":
            raise PermissionDenied(
                "The Administrator role cannot be edited here."
            )

        serializer.save()

    def perform_destroy(self, instance):
        self.check_admin()

        if instance.name == "Administrator":
            raise PermissionDenied(
                "The Administrator role cannot be deleted."
            )

        if instance.users.exists():
            raise PermissionDenied(
                "Cannot delete a role assigned to users."
            )

        instance.delete()
