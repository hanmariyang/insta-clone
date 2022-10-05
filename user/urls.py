#user.urls.py

from django.urls import path
from . import views
from .views import UploadProfile

urlpatterns = [
    path('sign-up/', views.sign_up_view,name='sign-up'),
    path('sign-in/', views.sign_in_view,name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('user/edit/<int:id>/', views.profile_edit, name='profile-edit'),
    path('user/password-edit/<int:id>/', views.change_password, name='password-edit'),
    path('profile/user/profile/upload/', UploadProfile.as_view()),
    path('user/', views.user_view, name='user-list'), 
    path('user/follow/<int:id>/', views.user_follow, name='user-follow'),
]