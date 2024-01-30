from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.validators import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SignUpSerializer(ModelSerializer):
    username = CharField(write_only=True, max_length=150)
    password = CharField(write_only=True, max_length=128)
    password_check = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "role", "password", "password_check"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_check"]:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        if validated_data.get("role") == "superuser":
            validated_data["is_active"] = True
            validated_data["is_staff"] = True
            validated_data["is_superuser"] = True
        validated_data.pop("password_check")
        user = User.objects.create_user(**validated_data)
        return user


class LogInSerializer(serializers.Serializer):
    username = CharField(write_only=True, max_length=150)
    password = CharField(write_only=True, max_length=128)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            if user is None:
                raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User is not active.")
        return {"user": user}