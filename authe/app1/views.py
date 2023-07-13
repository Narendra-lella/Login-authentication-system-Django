from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth import authenticate,login

from .email import send_mail_password
import uuid #for creating unique tokens
# Create your views here.

def page1(request):
    return render( request, 'welcomepage.html')

def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        upass1 = request.POST['upass1']
        upass2 = request.POST['upass2']
  
        if  User.objects.filter(username = username).exists():
            messages.error(request, 'Username  is already in use ,try another')
            return redirect('/register/')
        
        if  User.objects.filter(email = email).exists():
            messages.error(request, ' email is already in use ,try another')
            return redirect('/register/')
        
        if upass1!=upass2:
            messages.error(request, "password didn't match")
            return redirect('/register/')

        myuser = User.objects.create_user( username, email, upass1)

        myuser.save()
        messages.success(request, 'account is created successfully')
        return redirect('/login_page/')
    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        upass1 = request.POST['upass1']


        user = authenticate(username = username, password = upass1)

        if user:
            login(request, user)
            messages.success(request, 'logined successfully')
            return redirect('/home/')
        else:
            messages.error(request, 'wrong username/password. please try again')
            return redirect('/login_page/')     
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def forgetpassword(request):

    try:
        if request.method == "POST":
            email = request.POST['email']

            if not User.objects.filter(email = email).first():
                messages.error(request, 'no user found with given emial id. Plesae tru again')
                return redirect('/forgetpassword/')
            user_obj = User.objects.get(email = email)
            token = str(uuid.uuid4())
            send_mail_password( user_obj, token)
            messages.success(request, 'An Emial is sent to  the given email Id. reset the password from there')
            return redirect('/login_page/')

    except Exception as e:
        print(e)
    return render(request, 'forgetpassword.html')


def changepassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.get(forget_password_token = token)
        print(profile_obj)

    
    except Exception as e:
        print(e)
    return render(request, 'changepassword.html')