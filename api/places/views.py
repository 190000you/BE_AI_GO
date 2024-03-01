from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Place, Tag, Review
from .serializers import PlaceModelSerializer, TagModelSerializer, ReviewModelSerializer

# Create your views here.


class PlaceView(ModelViewSet):
    serializer_class = PlaceModelSerializer
    queryset = Place.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = list()
        action = self.action
        
        if action == 'list' or action == 'retrieve':
            permission_classes = [AllowAny]
        elif action in ['create' , 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
class TagView(ModelViewSet):
    serializer_class = TagModelSerializer
    queryset = Tag.objects.all()


class ReviewView(ModelViewSet):
    serializer_class = ReviewModelSerializer
    queryset = Review.objects.all()

