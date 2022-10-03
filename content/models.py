from django.db import models


# Create your models here.
class Feed(models.Model):
    content = models.TextField()    # 글내용
    image = models.TextField()  # 피드 이미지
    user_id = models.TextField()
    like_count = models.IntegerField()
    profile_image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)