from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,username, email,password = None):
        '''Creating User'''
        if not username:
            raise ValueError("username is required")
        
        if not email:
            raise ValueError("Email Field is Requird.")

        email = self.normalize_email(email)

        user = self.model(username = username,email = email)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self,username,email,password = None):
        user = self.create_user(username,email,password)
        user.is_admin = True
        user.save(using = self._db)
        return user
    