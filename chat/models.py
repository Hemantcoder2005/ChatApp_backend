from django.db import models
from accounts.models import CustomUser as User
import uuid

# groups
class ChatRoom(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_chatrooms')
  
class GroupSubscription(models.Model):
    subscription_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'chatroom')

    def __str__(self):
        return f"{self.user.username} in {self.chatroom.name}"

class GroupPrivileges(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]
    privilege_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.OneToOneField(GroupSubscription, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    can_delete_messages = models.BooleanField(default=False)
    can_add_members = models.BooleanField(default=False)
    can_remove_members = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subscription.user.username} - {self.role} in {self.subscription.chatroom.name}"
    

# personal rooms
class PersonalChatroom(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_personal_chat')
        ]

    def __str__(self):
        return f"{self.chat_id}"
    

# message
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    sender = models.ForeignKey(User,on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default = False)

    chatroom_group = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,null=True,blank=True)
    chatroom_private = models.ForeignKey(PersonalChatroom,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.sender.username} -- > {self.text[:30]}"
    


class MessageTracker(models.Model):
    messageTrackerID = models.UUIDField(primary_key=True,default=uuid.uuid4(),editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    group_chatroom = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,null=True,blank=True)
    private_chatroom = models.ForeignKey(PersonalChatroom,on_delete=models.CASCADE,null=True,blank=True)

    message = models.ForeignKey(Message,on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('not_delivered', 'Not Delivered'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_delivered')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'message'], name='messageTracker')
        ]
    def __str__(self):
        return f"{self.user.username} - {self.message.text[:30]} ({self.status})"