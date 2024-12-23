from django.db import models
from django.contrib.auth.models import AbstractUser
from .CustomUserManager import CustomUserManager
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
    profile_picture = models.ImageField(upload_to='profile_pics/',null=True,blank=True,default='profile_pics/default.jpg')
    bio = models.TextField(null = True,blank=True)
    isOnline = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.email
    
    @property
    def is_superuser(self):
        return self.is_admin