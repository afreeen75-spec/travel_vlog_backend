import random
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


def send_otp_email(user, otp_code):
    subject = "Your OTP code"
    message = (
        f"Hello {user.username},\n\n"
        f"Your OTP verification code is {otp_code}.\n"
        "Use it to complete your login."
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    if not user.email:
        return False

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True
    except Exception:
        return False

from .models import OTP


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_obj = User.objects.filter(username__iexact=attrs["username"]).first()
        if not user_obj:
            raise serializers.ValidationError("Invalid username or password")

        user = authenticate(username=user_obj.username, password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        otp_code = f"{random.randint(100000, 999999)}"
        OTP.objects.filter(user=user).delete()
        otp_obj = OTP.objects.create(user=user, otp_code=otp_code)
        email_sent = send_otp_email(user, otp_code)

        detail = (
            "OTP sent to your email. Please verify it to complete login."
            if email_sent
            else "OTP generated successfully. Please use the code shown below to complete login."
        )

        return {
            "detail": detail,
            "user_id": user.id,
            "otp_id": otp_obj.id,
            "otp_code": otp_code,
            "email_sent": email_sent,
        }


class VerifyOTPSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(username__iexact=attrs["username"]).first()
        if not user:
            raise serializers.ValidationError("User not found")

        otp_obj = OTP.objects.filter(user=user, otp_code=attrs["otp"]).order_by("-created_at").first()
        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired")

        refresh = RefreshToken.for_user(user)
        otp_obj.delete()
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }