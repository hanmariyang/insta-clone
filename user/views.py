from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 있는지 검사하는 함수
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import update_session_auth_hash

def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        nickname = request.POST.get('nickname', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        if password != password2:
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if email == '' or password == '':
                return render(request, 'user/signup.html', {'error': '이메일과 패스워드를 입력해주세요.'})
            
            exist_email = get_user_model().objects.filter(email=email)
            if exist_email:
                return render(request, 'user/signup.html', {'error': '이미 존재하는 이메일입니다.'})
            else:
                UserModel.objects.create_user(email=email, username=username, password=password, nickname=nickname)
                return redirect('/sign-in') # 회원가입이 완료되었으므로 로그인 페이지로 이동
    

# user/views.py
def sign_in_view(request):
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

@login_required
def change_password(request):  #비밀번호 변경
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'content/profile.html')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'user/change_password.html', context)