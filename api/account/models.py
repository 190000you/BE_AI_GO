from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager as DjangoUserManager,
)

from survey.models import Answer

# # Create your models here.


# class CustomUserManager(BaseUserManager):
#     def _create_user(self, username, password, **extra_fields):
#         if not username:
#             raise ValueError("아이디를 입력해주세요.")

#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_user(self, username, password=None, **other_fields):
#         user = self.model(username=username, **other_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, username, password=None, **other_fields):
#         other_fields.setdefault("is_staff", True)
#         other_fields.setdefault("is_superuser", True)
#         other_fields.setdefault("is_active", True)

#         if other_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must be assigned to is_staff=True.")
#         if other_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must be assigned to is_superuser=True")

#         return self.create_user(username, password, **other_fields)


# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)

#     start_date = models.DateTimeField(default=timezone.now)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     objects = CustomUserManager()

#     USERNAME_FIELD = "username"

#     def __str__(self):
#         return self.username


class UserManager(DjangoUserManager):
    def _create_user(self, userId, userPassword, **extra_fields):
        if not userId:
            raise ValueError("아이디를 입력해주세요.")

        user = self.model(userId=userId, **extra_fields)
        user.set_password(userPassword)
        user.save(using=self._db)

        return user

    def create_user(self, userId, userPassword=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(userId, userPassword, **extra_fields)

    def create_superuser(self, userId, userPassword=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(userId, userPassword, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # ROLES = (("User", "user"), ("superuser", "manager"))

    # role = models.CharField(max_length=20, choices=ROLES, default="user")
    userEmail = models.CharField(max_length=150)
    userId = models.CharField(max_length=150, primary_key=True)
    userName = models.CharField(max_length=150)
    userPassword = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    
    # is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    survey = models.OneToOneField(Answer, on_delete=models.CASCADE, null=True)

    REQUIRED_FIELDS = ['userEmail', 'userName']
    objects = UserManager()
    USERNAME_FIELD = "userId"
