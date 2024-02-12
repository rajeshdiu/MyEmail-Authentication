from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Custom_User(AbstractUser):
    user_type=[
        ('admin','Admin'),('student','Student')
    ]
    display_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    user_type=models.CharField(choices=user_type,max_length=120)
    
    def __str__(self):
        return self.display_name

