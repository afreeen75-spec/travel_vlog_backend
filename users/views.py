import json

from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ActivityLog
from .serializers import LoginSerializer, RegisterSerializer, VerifyOTPSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        ActivityLog.objects.create(
            user=response.data.get("id") and User.objects.filter(id=response.data["id"]).first(),
            action="Register",
            details="User registered successfully",
            ip_address=self._get_client_ip(request),
        )
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        data = self._get_request_data(request)
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ActivityLog.objects.create(
            user=User.objects.filter(username__iexact=data.get("username")).first(),
            action="Login",
            details="Login initiated and OTP sent",
            ip_address=self._get_client_ip(request),
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def _get_request_data(self, request):
        try:
            return request.data
        except Exception:
            pass

        if request.body:
            try:
                body = request.body.decode("utf-8")
                if body:
                    parsed = json.loads(body)
                    if isinstance(parsed, dict):
                        return parsed
            except (TypeError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
                pass

        if request.POST:
            return request.POST.dict()

        return {}

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class VerifyOTPView(APIView):
    authentication_classes = []

    def post(self, request):
        data = self._get_request_data(request)
        serializer = VerifyOTPSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ActivityLog.objects.create(
            user=User.objects.filter(username__iexact=data.get("username")).first(),
            action="OTP Verification",
            details="OTP verified successfully",
            ip_address=self._get_client_ip(request),
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def _get_request_data(self, request):
        try:
            return request.data
        except Exception:
            pass

        if request.body:
            try:
                body = request.body.decode("utf-8")
                if body:
                    parsed = json.loads(body)
                    if isinstance(parsed, dict):
                        return parsed
            except (TypeError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
                pass

        if request.POST:
            return request.POST.dict()

        return {}

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        ActivityLog.objects.create(
            user=request.user,
            action="Logout",
            details="User logged out",
            ip_address=self._get_client_ip(request),
        )
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
