# tweet/urls.py
from django.urls import path, include
from . import views
from .views import UploadFeed, profile

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('content/', views.content, name='content'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('content/upload', UploadFeed.as_view()),
    path('content/delete/<int:id>', views.DeleteFeed, name="DeleteFeed"),
    path('content/modify/<int:id>/', views.modify, name='content-modify'),
    path('profile/edit/', views.profile_edit_page, name='profile_edit_page'),
    path('profile/edit/password/', views.profile_edit_password, name='profile_edit_password'),
    path('search/', views.search,name='search'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
    path('profile/', profile.as_view()),
    path('tweet/<int:id>/', views.detail_tweet, name="detail_tweet"), #댓글
    path('tweet/comment/<int:id>/', views.write_comment, name="write_comment"), #댓글작성
]