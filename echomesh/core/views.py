from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import *
from django.http import QueryDict
from django.http import JsonResponse
from django.contrib import messages
from functools import partial
import json
from django.db.models import Q
from.utils import publitio_file_upload



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


def check_post_activity(post_obj,current_user):
    resp={}
    like_obj=Like.objects.filter(user=current_user,post=post_obj).first()
    like_count=Like.objects.filter(post=post_obj).count
    comment_obj=Comment.objects.filter(user=current_user,post=post_obj).first()
    comment_count=Comment.objects.filter(post=post_obj).count
    share_obj=Share.objects.filter(user=current_user,post=post_obj).first()
    save_obj=Save.objects.filter(user=current_user,post=post_obj).first()
    resp['post']=post_obj
    resp['like_count']=like_count
    resp['comment_count']=comment_count
    if like_obj:
        resp['current_user_liked']=True
    else:
        resp['current_user_liked']=False
    if comment_obj:
        resp['current_user_commented']=True
    else:
        resp['current_user_commented']=False
    if share_obj:
        resp['current_user_shared']=True
    else:
        resp['current_user_shared']=False
    if save_obj:
        resp['current_user_saved']=True
    else:
        resp['current_user_saved']=False
    return resp

@login_required
def home(request):
    user=request.user
    posts_obj=Post.objects.filter(user=user).order_by('-created_at')
    post_obj_final = list(map(partial(check_post_activity, current_user=user), posts_obj))
    post_count=len(posts_obj)
    
    context={'posts':post_obj_final,
    "user":user,
    "post_count":post_count}

    return render(request,'core/index.html',context)



@login_required
def like_post(request):
    user=request.user
    request_body= QueryDict(request.body)
    resp={"Response":"Success"}
    try:
        json_data = json.loads(list(request_body.keys())[0]) 
        post_id=json_data.get('post_id')
        like_obj=Like()
        like_obj.post = Post.objects.filter(id=post_id).first()
        like_obj.user = user
        like_obj.save()
    except:
        resp['Response':"Error"]
    return JsonResponse(resp)



@login_required
def dislike_post(request):
    user=request.user
    request_body= QueryDict(request.body)
    resp={"Response":"Success"}
    try:
        json_data = json.loads(list(request_body.keys())[0]) 
        post_id=json_data.get('post_id')
        like_obj=Like.objects.filter(Q(user=user)&Q(post=Post.objects.filter(id=post_id).first())).first()
        like_obj.delete()
    except:
        resp['Response':"Error"]
    return JsonResponse(resp)


@login_required
def upload_post(request):
    user=request.user
    text=request.POST.get('text','')
    image=request.FILES.get('image','')
    video=request.FILES.get('video','')
    image_url=None
    video_url=None
    if image:
        post_type='Image'
        image1_resp =publitio_file_upload(bytedata=image,folder_id='jp2rRmM4',title=f"post by {user.first_name}")
        if image1_resp['file_url']:
            if image1_resp['file_url'] != 'File upload is not successfull. Please try again':
                image_url = image1_resp['file_url']
    elif video:
        post_type='Video'
    else:
        post_type='Text'

    return redirect('home')
