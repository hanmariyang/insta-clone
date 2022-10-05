#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):

    class Meta:
        db_table = "my_user" # 여기는 테이블 이름이에요! 꼭 기억 해 주세요!
        
        
    email = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
    username = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50, blank=True)
    profile_image = models.TextField()
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']
    
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee')
    