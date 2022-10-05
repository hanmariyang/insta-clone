from django.contrib import admin
from .models import TweetComment, Feed

admin.site.register(Feed)
admin.site.register(TweetComment)

# Register your models here.
