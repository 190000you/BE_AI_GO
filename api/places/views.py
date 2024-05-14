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
    queryset = Place.objects.none()  # 빈 쿼리셋 할당
    def post(self, request):
        name = request.data.get('name', '')

        if not name:
            return Response({'error': 'No name provided'}, status=status.HTTP_400_BAD_REQUEST)

        # name을 사용하여 장소 이름과 태그를 검색
        tag = '#' + name  # 태그 값이 들어온다면 # 붙여서 검사
        places_by_name = Place.objects.filter(name__contains=name)
        places_by_tag = Place.objects.filter(tag=tag)

        # 장소 이름으로 검색한 결과
        serializer_name = PlaceModelSerializer(places_by_name, many=True)
        # 태그로 검색한 결과
        serializer_tag = PlaceModelSerializer(places_by_tag, many=True)

        # 응답 데이터 구성
        response_data = {
            'places_by_name': serializer_name.data,
            'places_by_tag': serializer_tag.data
        }

        # 하나라도 결과가 있다면 OK 응답, 그렇지 않으면 NOT FOUND 응답
        if places_by_name.exists() or places_by_tag.exists():
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No place found with this name or tag'}, status=status.HTTP_404_NOT_FOUND)