from django.shortcuts import render

from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import User
from places.models import Review, Place
from places.serializers import ReviewModelSerializer
from .serializers import SignUpSerializer, UserModelSerializer, UserDetailSerializer, LogInSerializer, AuthSerializer, ChangePassWordSerializer, UserLikePlaceSerializer, UserLikePlaceViewSerializer
from permission import IsOnerAdminUser

# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserDetailView(generics.RetrieveAPIView):

    authentication_classes = [JWTAuthentication] # 1. 토큰인증된 사람만 접근
    permission_classes = [IsAuthenticated, IsOnerAdminUser] # 2. 인증된 사람 중에서 자기 자신, admin유저만 접근
    queryset = User.objects.all()

    lookup_url_kwarg = 'userId'
    def get_serializer_class(self):
        return UserDetailSerializer if self.request.method == 'GET' else UserModelSerializer
    
    def get_object(self):
        userId = self.kwargs.get('userId')
        return get_object_or_404(User, userId=userId)

class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewModelSerializer

    authentication_classes = [JWTAuthentication] # 1. 토큰인증된 사람만 접근
    permission_classes = [IsAuthenticated, IsOnerAdminUser] # 2. 인증된 사람 중에서 자기 자신, admin유저만 접근

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        userId = self.kwargs.get('userId')
        user = get_object_or_404(User, userId=userId)
        return Review.objects.filter(writer=user)
    
    def get_object(self):
        userId = self.kwargs.get('userId')
        return get_object_or_404(User, userId=userId)
    
class UserSignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # 사용할 시리얼라이저 변수에 넣고
        if serializer.is_valid(raise_exception=True): # 유효성 검사
            user = serializer.save() # 통과하면 저장
            user.set_password(serializer.validated_data['userPassword']) # 비밀번호 암호화
            user.save()

            token = TokenObtainPairSerializer.get_token(user) # 토큰 발급
            refresh_token = str(token) 
            access_token = str(token.access_token)

            res_data = {
                "user": serializer.data,
                "message": "register success",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }
            res = Response(res_data, status=status.HTTP_201_CREATED) # json형태로 응답
            res.set_cookie("access", access_token, httponly=True) # 쿠키에 access, refresh 토큰 저장
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유효성 검사 통과 못하면 오류

class UserLogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_data_serializer = UserModelSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res_data = {
                "user": user_data_serializer.data,
                "message": "login success",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }
            
            response = Response(res_data, status=status.HTTP_200_OK)
            response.set_cookie("access", access_token, httponly=True)
            response.set_cookie("refresh", refresh_token, httponly=True)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(generics.GenericAPIView):
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_data_serializer = UserModelSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res_data = {
                "user": user_data_serializer.data["userId"],
                "message": "login success",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }
            
            response = Response(res_data, status=status.HTTP_200_OK)
            response.set_cookie("access", access_token, httponly=True)
            response.set_cookie("refresh", refresh_token, httponly=True)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePassWordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(): # 유효성 검사
            serializer.update(serializer.validated_data['user'], serializer.validated_data) # 비밀번호 변경
            return Response("password changing complete!", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ## 장소 찜하기
class UserLikeRegView(generics.GenericAPIView):
    serializer_class = UserLikePlaceSerializer
    authentication_classes = [JWTAuthentication]

    # post매서드를 사용할때 로직
    def post(self, request):
        # 장소 이름을 받아와서
        place_name = request.data.get('name')
        # 디비에서 일치하는 장소를 찾기
        place = get_object_or_404(Place, name=place_name)
        # 해당하는 데이터의 like 칼럼에 좋아요 누른 user 추가
        place.like.add(request.user)
        # 변경사항 저장
        place.save()

        # 응답용 시리얼라이저 
        serializer = self.get_serializer(place)
        # 제대로 됐다는 응답
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    ## 찜 한 장소 조회
class UserLikeView(generics.GenericAPIView):
    serializer_class = UserLikePlaceViewSerializer
    authentication_classes = [JWTAuthentication]

    # get 매서드 사용할 때
    def get(self, request):
        # 디비에서 filter를 사용하여 로그인 한 유저에 해당하는 한개 또는 여러개의 장소 찾기
        # objects.get 을 하면 안됨. 여러개의 장소가 return 될 수 있기때문
        like_place = Place.objects.filter(like=request.user)
        # many=True를 해주는 이유는 시리얼라이저는 단일 인스턴스를 처리하게 설계됐는데, 여러개의 인스턴스를 처리하기위해 many=True 속성을 준다
        serializer = self.get_serializer(like_place, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)