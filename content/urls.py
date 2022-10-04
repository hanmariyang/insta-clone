# tweet/urls.py
from django.urls import path
from . import views
from .views import UploadFeed

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('content/', views.content, name='content'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('profile/', views.profile, name='profile'),
    path('content/upload', UploadFeed.as_view()),
    path('content/delete/<int:id>', views.DeleteFeed, name="DeleteFeed")
]