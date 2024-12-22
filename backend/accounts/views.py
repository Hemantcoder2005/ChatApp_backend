from django.shortcuts import render
from .serializer import CustomUserSerializer
from .models import CustomUser
from rest_framework import generics


class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self,request,*args,**kwargs):
        reponse = super().create(request,*args,**kwargs)
        reponse.data['message'] = "User Created Successfully"
        return reponse