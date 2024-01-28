from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import *

def login(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        print("username",username,"password",password)
        user = authenticate(username=username, password=password)
        print("user",user)
        if user is not None:
            auth_login(request,user)
            print("loggedin")
            return redirect('home')
        else:
            context={}
            return render(request,'core/login.html',context)
    context={}
    return render(request,'core/login.html',context)

@login_required
def logout_view(request):
    print("req-")
    logout(request)
    return redirect('login')



def registration_view(request):

    firstname=request.POST.get('firstname','')
    lastname=request.POST.get('lastname','')
    email=request.POST.get('email','')
    username=email
    password=request.POST.get('password','')

    print("-",firstname,lastname,email,password)

    try:
        user = User.objects.create_user(username=username,password=password,email=email,first_name=firstname,last_name=lastname)
        auth_login(request,user)
        return redirect('home')
    except IntegrityError as e:
        if "UNIQUE constraint failed: auth_user.username" in str(e):
            messages.error(request, "Email already exists.")
            return redirect('login')
    except Exception as e:
        messages.error(request, "An Error Occured.")
        return redirect('login')
    return redirect('home')



@login_required
def home(request):
    user=request.user
    posts_obj=Post.objects.filter(user=user).order_by('-created_at')
    context={'posts':posts_obj,
    "user":user}
    return render(request,'core/index.html',context)