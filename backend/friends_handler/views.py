from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts import models
from notification.views import send_notification 
User = models.CustomUser
# Create your views here.
def sendRequest():
    pass

def removeRequest():
    pass


class RequestManager(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            user1 = request.user
            user2_email = request.data.get("user")
            if not user2_email:
                return Response({"error":True,"mssg":"Invalid email!"})
            try:
                user2 = User.objects.get(email = user2_email)
            except User.DoesNotExist:
                return Response({"error":True,"mssg":"email doesn't exist"})
            print(user1,user2)
            user1.send_request(user2)
            return Response({"error":False,"mssg":"Successfully requested!"})
             
        except Exception as e:
            print(e)
            return Response({"error":True,"mssg":"Internal Server error!"})
    def delete(self,request):
        try:
            user1 = request.user
            user2_email = request.data.get("user")
            if not user2_email:
                return Response({"error":True,"mssg":"Invalid email!"})
            try:
                user2 = User.objects.get(email = user2_email)
            except User.DoesNotExist:
                return Response({"error":True,"mssg":"email doesn't exist"})
            print(user1,user2)
            user1.remove_request(user2)
            return Response({"error":False,"mssg":"Successfully removed!"})
             
        except Exception as e:
            print(e)
            return Response({"error":True,"mssg":"Internal Server error!"})
class FriendManager(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            user1 = request.user
            user2_email = request.data.get("user")
            if not user2_email:
                return Response({"error":True,"mssg":"Invalid email!"})
            try:
                user2 = User.objects.get(email = user2_email)
            except User.DoesNotExist:
                return Response({"error":True,"mssg":"email doesn't exist"})
            if user1.addFriend(user2):
                return Response({"error":False,"mssg":"request accepted"})
            return Response({"error":True,"mssg":"you are accepting request that is never made."})
        except Exception as e:
            print(e)
            return Response({"error":True,"mssg":"Internal Server error!"})
    def delete(self,request):
        try:
            user1 = request.user
            user2_email = request.data.get("user")
            if not user2_email:
                return Response({"error":True,"mssg":"Invalid email!"})
            try:
                user2 = User.objects.get(email = user2_email)
            except User.DoesNotExist:
                return Response({"error":True,"mssg":"email doesn't exist"})
            if user2.removeFriend(user1):
                return Response({"error":False,"mssg":"friend removed successfully!"})
            return Response({"error":True,"mssg":"you are removing friend that is never made."})
             
        except Exception as e:
            print(e)
            return Response({"error":True,"mssg":"Internal Server error!"})