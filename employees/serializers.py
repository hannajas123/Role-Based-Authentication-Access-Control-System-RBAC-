
from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )
    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "username",
            "email",
            "department",
            "designation",
            "phone",
            "address",
            "date_of_joining",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee_id",
            "username",
            "email",
            "created_at",
            "updated_at",
        ]

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from roles.models import Role
from .models import Employee

User = get_user_model()


class EmployeeCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = Employee
        fields = [
            "username",
            "email",
            "password",
            "employee_id",
            "department",
            "designation",
            "phone",
            "address",
            "date_of_joining",
        ]

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "This username already exists."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email already exists."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        employee_role = Role.objects.get(name="Employee")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=employee_role,
        )

        employee = Employee.objects.create(
            user=user,
            **validated_data
        )

        return employee
    
    def to_representation(self, instance):
        return EmployeeSerializer(
            instance,
            context=self.context
        ).data
