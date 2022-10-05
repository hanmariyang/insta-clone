# tweet/urls.py
from django.urls import path, include
from . import views
from .views import UploadFeed

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('content/', views.content, name='content'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('content/upload', UploadFeed.as_view()),
    path('content/delete/<int:id>', views.DeleteFeed, name="DeleteFeed"),
    path('content/modify/<int:id>/', views.modify, name='modify'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit_page, name='profile_edit_page'),
    path('profile/edit/password/', views.profile_edit_password, name='profile_edit_password'),
]