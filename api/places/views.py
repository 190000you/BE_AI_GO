from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Place, Tag, Review
from .serializers import PlaceModelSerializer, TagModelSerializer, ReviewModelSerializer, PlaceSearchSerializer

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

class PlaceFindView(generics.GenericAPIView):
    serializer_class = PlaceSearchSerializer
    queryset = ''

    def post(self, request):
        name = request.data.get('name')
        if name:
            place = Place.objects.filter(name=name)
            if not place.exists():
                return Response({'error': 'No place found with this name'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PlaceModelSerializer(place, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No name provided'}, status=status.HTTP_400_BAD_REQUEST)


