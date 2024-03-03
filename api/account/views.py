from django.shortcuts import render

from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.shortcuts import get_object_or_404

from .models import User
from places.models import Review
from places.serializers import ReviewModelSerializer
from .serializers import SignUpSerializer, UserModelSerializer, UserDetailSerializer, LogInSerializer, AuthSerializer, ChangePassWordSerializer

# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    lookup_url_kwarg = 'uid'
    def get_serializer_class(self):
        return UserDetailSerializer if self.request.method == 'GET' else UserModelSerializer
    
    def get_object(self):
        uid = self.kwargs.get('uid')
        return get_object_or_404(User, uid=uid)

class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewModelSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        uid = self.kwargs.get('uid')
        user = get_object_or_404(User, uid=uid)
        return Review.objects.filter(writer=user)
    
    def get_object(self):
        uid = self.kwargs.get('uid')
        return get_object_or_404(User, uid=uid)
    
class UserSignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()

            token = TokenObtainPairSerializer.get_token(user)
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
            res = Response(res_data, status=status.HTTP_201_CREATED)
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                "user": user_data_serializer.data["username"],
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

        if serializer.is_valid():
            serializer.update(serializer.validated_data['user'], serializer.validated_data)
            return Response("password changing complete!", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)