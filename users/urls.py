from django.urls import path
from .views import ActivityLogListView, LoginView, LogoutView, RegisterView, VerifyOTPView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activity-logs/", ActivityLogListView.as_view(), name="activity-logs"),
]