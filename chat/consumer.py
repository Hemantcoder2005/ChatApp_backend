import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from .models import *
from channels.db import database_sync_to_async
from .serializer import *
class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.chatRoomID = None
        self.isPrivateRoom = False
        self.chatRoom = None
        self.loadPointer = 0
    async def send_mssg(self, type, message):
        """Send a WebSocket message to the client."""
        await self.send(
            text_data=json.dumps({
                'type': type,
                'message': message
            })
        )

    @database_sync_to_async
    def checkRoom(self):
        """Check if the chatroom exists and the user is a part of it."""
        chatRoomInstance = self.chatRoom.first()
        return chatRoomInstance and (chatRoomInstance.user1 == self.user or chatRoomInstance.user2 == self.user)

    @database_sync_to_async
    def isValidChatRoom(self, chatRoomid):
        """Check if the chatroom exists and the user belongs to it."""
        self.chatRoom = PersonalChatroom.objects.filter(chat_id=chatRoomid)
        if not self.chatRoom.exists():
            return False
        if self.checkRoom():
            self.chatRoom = self.chatRoom.first()
            self.isPrivateRoom = True
            return True

        self.chatRoom = ChatRoom.objects.filter(chat_id=chatRoomid)
        if self.checkRoom():
            self.chatRoom = self.chatRoom.first()
            return True

        self.chatRoom = None
        return False

    @database_sync_to_async
    def saveMssg(self, mssg):
        """Store message in the database."""
        try:
            if not self.isPrivateRoom:
                Message.objects.create(text=mssg, sender=self.user, chatroom_group=self.chatRoom)
            else:
                Message.objects.create(text=mssg, sender=self.user, chatroom_private=self.chatRoom)
        except Exception as e:
            print(f"Error saving message: {e}")

    @database_sync_to_async
    def load_chats(self):
        """Help in loading chats with help of chatroom Instance when user connect to room"""
        data = None
        if self.isPrivateRoom:
            data = Message.objects.filter(chatroom_private = self.chatRoom)
        else:
            data = Message.objects.filter(chatroom_group = self.chatRoom)
        data = data.order_by('-timestamp')
        self.chatHistory = ChatSerializer(data, many=True).data
        print("Chat Loaded Successfully!")


    async def send_chat_history(self,limit):
        """Placeholder for sending previous chat messages (Not implemented yet)."""
        if len(self.chatHistory) <= self.loadPointer:
            return {}
        chats = self.chatHistory[self.loadPointer:min(self.loadPointer + limit,len(self.chatHistory))]
        self.loadPointer += limit
        return chats

    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope['user']
        chatroom = parse_qs(self.scope['query_string'].decode()).get("chatroomID", [None])[0]
        self.room_name = chatroom
        self.room_group_name = f'chat_{self.room_name}'

        isValidRoom = await self.isValidChatRoom(chatroom)
        print(isValidRoom)
        if self.user.is_authenticated and isValidRoom:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            print(f"{self.user.username} is connected to {self.room_group_name}.")
            await self.load_chats()
        else:
            await self.close()

    async def receive(self, text_data):
        """Receive messages from WebSocket and broadcast them."""
        try:
            text_data_json = json.loads(text_data)
            mssg = text_data_json['text']
            typeof = text_data_json['type']
            print(typeof)
            if typeof == 'ws.send':
                # Broadcast message to the group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": mssg,
                        "sender": self.user.username
                    }
                )

                # Save message to the database
                await self.saveMssg(mssg)

            elif typeof == "ws.history":
                try:
                    limit = int(text_data_json['limit'])
                    await self.send_mssg("ws.history",await self.send_chat_history(limit))

                except Exception as e:
                    print(e)
                    await self.send_mssg("ws.error","Error Occured while Loading chat history.")
                    

        except Exception as e:
            print(f"Error in receive: {e}")
            await self.send_mssg("ws.error", "Error occurred")

    async def chat_message(self, event):
        """Send messages to WebSocket clients."""
        message = event["message"]
        sender = event["sender"]

        await self.send(text_data=json.dumps({
            "type": "ws.mssg",
            "message": message,
            "sender": sender
        }))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()
