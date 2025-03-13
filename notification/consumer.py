from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        self.user_id = self.scope['user']
        print(self.user_id)
        self.room_name = f"notification_{self.user_id}"
        self.room_group_name = f"notification_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_name,
            self.room_group_name
        ) 
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.room_group_name
        )
    async def recieve(self):
        pass # we will not recieve mssg in notification
    async def send_notification(self,event):
        notification = event['notification'] # Assuming we will get json
        await self.send(text_data=notification) 