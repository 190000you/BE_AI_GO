from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from .serializers import EnrollmentSerializer
from .models import Answer
# Create your views here.

class AnswerView(ModelViewSet):
    serializer_class = EnrollmentSerializer
    queryset = Answer.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = list()
        action = self.action
        
        if action == ['list', ' create', 'retrieve']:
            permission_classes = [AllowAny]
        elif action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
