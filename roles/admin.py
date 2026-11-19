

from django.contrib import admin
from .models import Role, Permission
# Register your models here.


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "module", "action")
    list_filter = ("module",)
    search_fields = ("module", "action")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("permissions",)
