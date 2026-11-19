
from rest_framework import serializers
from .models import Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "module", "action"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        source="permissions",
        write_only=True,
        required=False
    )

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
            "permissions",
            "permission_ids",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
