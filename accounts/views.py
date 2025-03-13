from django.shortcuts import render
from .serializer import CustomUserSerializer
from .models import CustomUser
from rest_framework import generics
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)
class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self,request,*args,**kwargs):
        reponse = super().create(request,*args,**kwargs)
        reponse.data['message'] = "User Created Successfully"
        return reponse
    
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Authentication attempt: {request.data}")
        return super().post(request, *args, **kwargs)
    

class GetUserDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        print(user)
        serializer = CustomUserSerializer(user,exclude_fields=["password"])
        response = serializer.data
        print(type(response))
        return Response(response)