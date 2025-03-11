import json
from channels.generic.websocket import WebsocketConsumer
from urllib.parse import parse_qs
from .models import *

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.chatRoomID = None
        self.isPrivateRoom = False
        self.chatRoom = None
    def send_mssg(self,type,message):
        self.send(
            text_data=json.dumps(
                {
                    'type':type,
                    'message': message
                }
            )
        )
    
    def checkRoom(self):
        """Check if the chatroom exists and the user is a part of it."""
        chatRoomInstance = self.chatRoom.first()
        return chatRoomInstance and (chatRoomInstance.user1 == self.user or chatRoomInstance.user2 == self.user)

    def isValidChatRoom(self, chatRoomid):
        """Check if the chatroom exists and the user belongs to it."""
        self.chatRoom = PersonalChatroom.objects.filter(chat_id=chatRoomid)
        if self.checkRoom():
            self.isPrivateRoom = True
            return True

        self.chatRoom = ChatRoom.objects.filter(chat_id=chatRoomid)
        if self.checkRoom():
            return True

        self.chatRoom = None
        return False


    def send_chat_history(self):
        pass
    def connect(self):
        user = self.scope['user']
        self.user = user
        chatroom = parse_qs(self.scope['query_string'].decode()).get("chatroomID",[None])[0]
        if user.is_authenticated and self.isValidChatRoom(chatroom):
            self.accept()
        else:
            self.close()
        self.send_chat_history()

        
        
    def receive(self,text_data):
        try:

            text_data_json = json.loads(text_data)
            mssg = text_data_json['text']
            self.send(
                json.dumps(
                {
                    "type":"websocket.send",
                    "text":mssg
                }
            )
            )
        except Exception as e:
            self.send(
                json.dumps(
                {
                    "type":"websocket.error",
                    "text":"Error Occured"
                }
            )
            )
    def disconnect(self,close_code):
        self.close()