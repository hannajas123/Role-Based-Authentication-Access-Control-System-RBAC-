
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs["username_or_email"].strip()
        password = attrs["password"]

        user = User.objects.filter(
            Q(username__iexact=identifier) |
            Q(email__iexact=identifier)
        ).first()

        if (
            user is None
            or not user.is_active
            or not user.check_password(password)
        ):
            raise AuthenticationFailed(
                "Invalid username/email or password."
            )

        refresh = RefreshToken.for_user(user)

        role_name = user.role.name if user.role else None

        permissions = []
        if user.role:
            permissions = list(
                user.role.permissions.values_list(
                    "module", "action"
                )
            )

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role_name,
                "permissions": [
                    {"module": module, "action": action}
                    for module, action in permissions
                ],
            },
        }


from django.contrib.auth import get_user_model
from rest_framework import serializers
from roles.models import Role

User = get_user_model()


class UserManagementSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8
    )

    role_name = serializers.CharField(
        source="role.name",
        read_only=True
    )

    role_id = serializers.PrimaryKeyRelatedField(
        source="role",
        queryset=Role.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role_id",
            "role_name",
            "is_active",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        if not password:
            raise serializers.ValidationError({
                "password": "Password is required."
            })

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    def validate(self, attrs):
        request = self.context.get("request")

        if (
            request
            and self.instance
            and self.instance.pk == request.user.pk
            and "role" in attrs
        ):
            if attrs["role"] != self.instance.role:
                raise serializers.ValidationError(
                    "You cannot change your own role."
                )

        return attrs


from rest_framework import serializers
from .models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ["email_notifications", "theme"]
    