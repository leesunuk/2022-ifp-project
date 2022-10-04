from os import stat
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView

from rest_framework.generics import RetrieveAPIView
from .serializers import *
from .models import User, Post
from .renderers import UserJSONRenderer
from coffee import serializers
# Create your views here.
class UserCreateAPIView(APIView): # 회원가입 view
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserCreateSerializer
    
    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView): #로그인 view
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserReadAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserReadSerializer
    # renderer_classes = (UserJSONRenderer,)

    queryset = User.objects.all()

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    # renderer_classes = (UserJSONRenderer)
    serializer_class = UserUpdateSerializer
    
    def get(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        