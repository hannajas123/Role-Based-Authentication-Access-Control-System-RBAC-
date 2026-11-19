
from .models import UserSettings
from .serializers import UserSettingsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer

# Create your views here.

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            if str(token["user_id"]) != str(request.user.pk):
                return Response(
                    {"error": "This token does not belong to you."},
                    status=status.HTTP_403_FORBIDDEN
                )

            token.blacklist()

            return Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )



from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import UserManagementSerializer

User = get_user_model()


class IsAdministrator:
    @staticmethod
    def check(user):
        return (
            user.is_authenticated
            and (
                user.is_superuser
                or (
                    user.role is not None
                    and user.role.name == "Administrator"
                )
            )
        )


class UserListCreateView(ListCreateAPIView):
    serializer_class = UserManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not IsAdministrator.check(self.request.user):
            raise PermissionDenied("Administrator access required.")
        return User.objects.select_related("role").all()

    def perform_create(self, serializer):
        if not IsAdministrator.check(self.request.user):
            raise PermissionDenied("Administrator access required.")
        serializer.save()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not IsAdministrator.check(self.request.user):
            raise PermissionDenied("Administrator access required.")
        return User.objects.select_related("role").all()

    def perform_update(self, serializer):
        if not IsAdministrator.check(self.request.user):
            raise PermissionDenied("Administrator access required.")
        serializer.save()

    def perform_destroy(self, instance):
        if not IsAdministrator.check(self.request.user):
            raise PermissionDenied("Administrator access required.")

        if instance.is_superuser:
            raise PermissionDenied(
                "Superuser accounts cannot be deleted through this API."
            )

        instance.delete()


class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    required_module = "Settings"

    def get(self, request):
        from roles.permissions import HasModulePermission

        permission = HasModulePermission()
        if not permission.has_permission(request, self):
            return Response(
                {"error": "You do not have permission to view settings."},
                status=403
            )

        settings, created = UserSettings.objects.get_or_create(
            user=request.user
        )

        return Response(UserSettingsSerializer(settings).data)

    def patch(self, request):
        from roles.permissions import HasModulePermission

        self.required_action = "Edit"
        permission = HasModulePermission()

        if not permission.has_permission(request, self):
            return Response(
                {"error": "You do not have permission to edit settings."},
                status=403
            )

        settings, created = UserSettings.objects.get_or_create(
            user=request.user
        )

        serializer = UserSettingsSerializer(
            settings,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
