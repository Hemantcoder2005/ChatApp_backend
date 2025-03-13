from .models import *
from rest_framework import serializers
class ChatSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    class Meta:
        model = Message
        exclude = ['chatroom_private','chatroom_group']