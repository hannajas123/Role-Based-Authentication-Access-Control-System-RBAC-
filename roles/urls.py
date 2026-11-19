
from django.urls import path
from .views import EmployeePermissionTestView,RoleListCreateView,RoleDetailView

urlpatterns = [
    path(
        "employee-permission-test/",
        EmployeePermissionTestView.as_view(),
        name="employee-permission-test"
    ),
    path("roles/", RoleListCreateView.as_view(), name="role-list-create"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
]
