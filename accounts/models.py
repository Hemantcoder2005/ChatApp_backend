from django.db import models
from django.contrib.auth.models import AbstractUser
from .CustomUserManager import CustomUserManager
from cloudinary.models import CloudinaryField
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length= 100,unique=True)
    first_name = models.CharField(max_length=50,blank= True)
    last_name = models.CharField(max_length=50,blank=True)
    profile_picture = CloudinaryField('image', default='default.jpg',)
    bio = models.TextField(null = True,blank=True)
    isOnline = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    friends = models.ManyToManyField('self',symmetrical=True,blank=True)
    pendingRequest = models.ManyToManyField("self",symmetrical=False,blank = True,related_name="received_requests")
    requested = models.ManyToManyField("self",symmetrical=False,blank = True,related_name="sent_requests")
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.username
    
    @property
    def is_superuser(self):
        return self.is_admin

    def addFriend(self,user):
        """
        Add friends user in friends section 
        """
        if self !=user and self.pendingRequest.filter(id=user.id).exists():
            self.friends.add(user)
            user.remove_request(self)
            from chat.models import PersonalChatroom
            # creating Private ChatRoom them
            users = sorted([self,user],key=lambda p:p.username)
            PersonalChatroom.objects.create(user1 = users[0], user2 = users[1])
            return True
        return False
    def removeFriend(self,user):
        """
        Remove Friend
        """
        if self != user and self.are_friends(user):
            self.friends.remove(user)
            user.remove_request(self)
            from chat.models import PersonalChatroom
            # creating Private ChatRoom them
            users = sorted([self,user],key=lambda p:p.username)
            PersonalChatroom.objects.filter(user1=users[0], user2=users[1]).delete()
            return True
        return False
    def send_request(self,user):
        """
        Update pending request and requested field
        """
        if self!=user:
            user.pendingRequest.add(self)
            self.requested.add(user)
            return True
        return False
    def remove_request(self,user):
        if self!=user:
            user.pendingRequest.remove(self)
            self.requested.remove(user)
    def are_friends(self, user):
        return self.friends.filter(id=user.id).exists()