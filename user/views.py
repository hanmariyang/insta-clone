# user/views.py
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model #사용자가 있는지 검사하는 함수
from django.contrib import auth, messages # 사용자 auth 기능
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from uuid import uuid4
import os
from instagram.settings import MEDIA_ROOT
from rest_framework.response import Response
""" sign_up_view - 회원가입
    sign_in_view - 로그인
    logout - 로그아웃
    delete - 회원탈퇴
    profile_edit - 사용자 정보 수정
    change_password - 비밀번호 변경
    UploadProfile - 프로필 사진 변경
    user_view, user_follow - 팔로우, 팔로워

"""


def sign_up_view(request):  #회원가입
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        nickname = request.POST.get('nickname', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        profile_image = "logo.png"
        
        if password != password2:
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if email == '' or password == '':
                return render(request, 'user/signup.html', {'error': '이메일과 패스워드를 입력해주세요.'})
            
            exist_email = get_user_model().objects.filter(email=email)
            exist_nickname = get_user_model().objects.filter(nickname=nickname)
            if exist_email:
                return render(request, 'user/signup.html', {'error': '이미 존재하는 이메일입니다.'})
            elif exist_nickname:
                return render(request, 'user/signup.html', {'error': '이미 존재하는 닉네임입니다.'})
            else:
                UserModel.objects.create_user(email=email, username=username, password=password, nickname=nickname, profile_image=profile_image)
                return redirect('/sign-in') # 회원가입이 완료되었으므로 로그인 페이지로 이동
    
def sign_in_view(request): #로그인
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, email=email, password=password) # 사용자 불러오기
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')
        else: 
            return render(request,'user/signin.html',{'error':'이메일 혹은 패스워드를 확인 해 주세요'})  # 로그인 실패
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required
def logout(request):   #로그아웃 함수
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")

@login_required
def delete(request):   #회원탈퇴
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('/')


def profile_edit(request, id):  # 사용자 정보 수정(이름,닉네임,이메일)
    if request.method == 'POST':
        user = UserModel.objects.get(id=id)
        user.username = request.POST.get('username')
        # user.nickname = request.POST.get('nickname')
        user.email = request.POST.get('email')
        user.save()
        return redirect("/")

def change_password(request, id): # 비밀번호 수정
    if request.method == "POST":
        user = UserModel.objects.get(id=id)
        origin_password = request.POST["origin_password"]
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('profile')
            else:
                messages.error(request, 'Password not same')
        else:
            messages.error(request, 'Password not correct')
            return render(request, 'content/profile_edit_password.html')
    else:
        return render(request, 'content/profile_edit_password.html')


class UploadProfile(APIView): # 프로필 사진 업로드
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name
        id = request.data.get('id')

        user = UserModel.objects.filter(id=id).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)

# user/views.py 

@login_required  # 팔로우, 팔로워 
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required # 팔로우, 팔로워 
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')

