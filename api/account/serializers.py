from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.validators import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from places.models import Place


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'userEmail', 'userName', 'survey', 'is_active', 'is_superuser']

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

## 회원가입
class SignUpSerializer(ModelSerializer):
    userEmail = CharField(write_only=True, max_length=150)
    userId = CharField(write_only=True, max_length=128)
    userName = CharField(write_only=True, required=True)
    userPassword = CharField(write_only=True, required=True)
    userPasswordCheck = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["userEmail", "userId", "userName", "userPassword", "userPasswordCheck"]

    def validate(self, attrs):
        if attrs["userPassword"] != attrs["userPasswordCheck"]:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        #if validated_data.get("role") == "superuser":
        #    validated_data["is_active"] = True
        #    validated_data["is_staff"] = True
        #    validated_data["is_superuser"] = True
        validated_data.pop("userPasswordCheck")
        user = User.objects.create_user(**validated_data)
        return user
    
## 로그인
class LogInSerializer(serializers.Serializer):
    userId = CharField(write_only=True, max_length=150)
    userPassword = CharField(write_only=True, max_length=128)

    def validate(self, data):
        user = authenticate(username=data["userId"], password=data["userPassword"])
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User is not active.")
        return {"user": user}
    
class AuthSerializer(serializers.Serializer):
    userPassword= CharField(write_only=True, max_length=150)

    def validate(self, data):
        userPassword = data.get("userPassword")
        try:
            user = User.objects.get(userPassword=userPassword)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid userId")
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        data['user'] = user
        return data
    
class ChangePassWordSerializer(serializers.Serializer):
    new_password = CharField(write_only=True, max_length=128)
    check_new_password = CharField(write_only=True, max_length=128)

    def validate(self, data):
        userId = data.get("userId")
        try:
            user = User.objects.get(userId=userId)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid userId")
        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        if data["new_password"] != data["check_new_password"]:
            raise ValidationError({"password": "Password fields didn't match."})
        
        data['user'] = user
        return data
    
    def update(self, instance, validated_data):
        user = validated_data['user']
        user.set_password(validated_data["new_password"])
        user.save()
    
        return user
    
class UserLikePlaceSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all())

    class Meta:
        model = Place
        fields = ["name"]

class UserLikePlaceViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["name","image","classification","street_name_address"]