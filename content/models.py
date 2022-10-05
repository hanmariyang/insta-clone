from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.conf import settings

# Create your models h
# 
# ere.

class TaggedFeed(TaggedItemBase):
    content_object = models.ForeignKey('Feed', on_delete=models.CASCADE)
class Feed(models.Model):
    content = models.TextField()    # 글내용
    image = models.TextField()  # 피드 이미지
    user_id = models.TextField()
    like_count = models.IntegerField()
    profile_image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    ### 태그 추가 부분###
    tags = TaggableManager(through=TaggedFeed, blank=True)

    def __str__(self):
        return self.user_id

class TweetComment(models.Model):
    class meta :
        db_table = 'TweetComment'  

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE) #장고문서를 봐보니 자신을 Content이부분에 적으라 명시가 되어있다
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)