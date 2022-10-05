
from email.mime import image
from turtle import update
from uuid import uuid4
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
import os
from instagram.settings import MEDIA_ROOT


# Create your views here.

def home(request):
    if request.method == 'GET' :
        user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
        if user:
            feeds = Feed.objects.all().order_by('-created_at')
            return render(request, 'content/home.html', {'feeds': feeds})
        else:
            return redirect('/sign-in')


def content(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            feeds = Feed.objects.all().order_by('-created_at')
            return render(request, 'content/home.html', {'feeds': feeds})
        else:
            return redirect('/sign-in')


class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')
        
        created_at = request.data.get('created_at')
        updated_at = request.data.get('updated_at')

        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0, created_at=created_at, updated_at=updated_at)

        return Response(status=200)

def DeleteFeed(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect('/content')

def modify(request, id):
    if request.method == 'POST':
        feed = Feed.objects.get(id=id)
        feed.content = request.POST.get('content')
        feed.save()
        return redirect("/")

def profile(request):
    return render(request, 'content/profile.html')


def profile_edit_page(request):
    return render(request, 'content/profile_edit.html')


def profile_edit_password(request):
    if request.method == "GET":
        return render(request, 'content/profile_edit_password.html')