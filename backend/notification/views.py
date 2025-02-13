from django.shortcuts import render

# Create your views here.


from channels.layers import channel_layers
import json
from asgiref.sync import sync_to_async

def send_notification(user,notificationMssg):
    channel_layer = channel_layers()
    group_name = f"notification_notification_{user.id}"
    sync_to_async(channel_layer.group_send)(
        group_name,
        {
            'type':"send_notification",
            'notification':notificationMssg
        }
    )
