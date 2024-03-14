"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserListView, UserDetailView, UserSignUpView, UserLogInView, AuthView, ChangePasswordView, UserReviewListView

namespace = "account"

urlpatterns = [
    path("list/", UserListView.as_view()),
    path("list/<str:userId>", UserDetailView.as_view()),
    path("list/<str:userId>/reviews", UserReviewListView.as_view()),
    path("signup/", UserSignUpView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("userauth/", AuthView.as_view()),
    path("changepassword/", ChangePasswordView.as_view()),
]
