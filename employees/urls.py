
from django.urls import path
from .views import MyEmployeeProfileView,EmployeeListCreateView,EmployeeDetailView

urlpatterns = [
    path("me/", MyEmployeeProfileView.as_view(), name="my-profile"),
    path("", EmployeeListCreateView.as_view(), name="employee-list-create"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
]
