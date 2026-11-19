
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from roles.permissions import HasModulePermission
from .serializers import EmployeeSerializer, EmployeeCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Employee
from .serializers import EmployeeSerializer

# Create your views here.

class MyEmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee = Employee.objects.select_related("user").get(
                user=request.user
            )
        except Employee.DoesNotExist:
            raise NotFound("Your employee profile has not been created.")

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

class EmployeeListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasModulePermission]
    required_module = "Employee Management"

    def get_queryset(self):
        return Employee.objects.select_related("user").all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EmployeeCreateSerializer
        return EmployeeSerializer


class EmployeeDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasModulePermission]
    required_module = "Employee Management"

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.select_related("user").all()
