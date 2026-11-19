
from django.urls import path
from .views import LoginView, LogoutView,UserListCreateView,UserDetailView
from .views import UserSettingsView
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("settings/", UserSettingsView.as_view(), name="user-settings"),
]
