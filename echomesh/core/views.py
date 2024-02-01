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
from.utils import publitio_image_upload,publitio_video_upload
from itertools import chain
from django.urls import reverse
from datetime import datetime




def login(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        print("username",username,"password",password)
        user = authenticate(username=username, password=password)
        print("user",user)
        if user is not None:
            auth_login(request,user)
            user_obj= UserProfile.objects.filter(user=User.objects.filter(id=user.id).first()).first()
            user_obj.online=True
            user_obj.save()
            return redirect('home')
        else:
            context={}
            return render(request,'core/login.html',context)
    context={}
    return render(request,'core/login.html',context)

@login_required
def logout_view(request):
    user=request.user
    user_obj= UserProfile.objects.filter(user=User.objects.filter(id=user.id).first()).first()
    user_obj.online=False
    user_obj.save()
    logout(request)
    return redirect('login')



def registration_view(request):

    firstname=request.POST.get('firstname')
    lastname=request.POST.get('lastname')
    email=request.POST.get('email')
    username=email
    password=request.POST.get('password')
    day = int(request.POST.get('day'))
    month = int(request.POST.get('month'))
    year = int(request.POST.get('year'))
    gender=request.POST.get('gender')

    date_object = datetime(year, month, day)



    try:
        user = User.objects.create_user(username=username,password=password,email=email,first_name=firstname,last_name=lastname)
        userprofile= UserProfile()
        userprofile.user=user
        userprofile.cover_picture='https://media.publit.io/file/echocp/defaultcover.jpg'
        if gender == 'Male':
            userprofile.profile_picture='https://media.publit.io/file/echopp/man-4140048.png'
        else:
                userprofile.profile_picture='https://media.publit.io/file/echopp/woman-4140047.png'
        userprofile.dob=date_object
        userprofile.save()

        print("userprofile=",userprofile)
        print("userprofile above")
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
    share_count=Share.objects.filter(post=post_obj).count
    save_obj=Save.objects.filter(user=current_user,post=post_obj).first()
    save_count=Save.objects.filter(post=post_obj).count
    resp['post']=post_obj
    resp['like_count']=like_count
    resp['comment_count']=comment_count
    resp['user']=post_obj.user
    resp['share_count'] = share_count
    resp['save_count'] = save_count
    resp['shared'] = False
    
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




# def check_shared_post_activity(post_obj,current_user,shared_user):
#     resp={}
#     like_obj=Like.objects.filter(user=current_user,post=post_obj).first()
#     like_count=Like.objects.filter(post=post_obj).count
#     comment_obj=Comment.objects.filter(user=current_user,post=post_obj).first()
#     comment_count=Comment.objects.filter(post=post_obj).count
#     share_obj=Share.objects.filter(user=current_user,post=post_obj).first()
#     share_count=Share.objects.filter(post=post_obj).count
#     save_obj=Save.objects.filter(user=current_user,post=post_obj).first()
#     save_count=Save.objects.filter(post=post_obj).count
#     resp['post']=post_obj
#     resp['like_count']=like_count
#     resp['comment_count']=comment_count
#     resp['user']=post_obj.user
#     resp['share_count'] = share_count
#     resp['save_count'] = save_count
#     resp['shared'] = True
#     resp['shared_user'] = shared_user
#     if like_obj:
#         resp['current_user_liked']=True
#     else:
#         resp['current_user_liked']=False
#     if comment_obj:
#         resp['current_user_commented']=True
#     else:
#         resp['current_user_commented']=False
#     if share_obj:
#         resp['current_user_shared']=True
#     else:
#         resp['current_user_shared']=False
#     if save_obj:
#         resp['current_user_saved']=True
#     else:
#         resp['current_user_saved']=False
#     return resp






# @login_required
def home(request):
    user=request.user
    if not user.is_authenticated:
        return redirect('login')
    
    
    all_friends = set(chain(*Friendship.objects.filter(
        (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
    ).values_list('receiver', 'sender')))

    posts_obj = sorted(Post.objects.filter(user__in=all_friends), key=lambda x: x.created_at, reverse=True)



    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    print("online friends", online_friends)

    online_friends_sorted = sorted(
        online_friends,
        key=lambda usr: usr.userprofile.online if usr.userprofile else False,
        reverse=True
    )

  
    
    post_obj_final = list(map(partial(check_post_activity, current_user=user), posts_obj))
    post_count=len(posts_obj)
    online_friends_sorted_ids = [user.id for user in online_friends_sorted]
    friend_suggestions = User.objects.exclude(pk=user.id).exclude(pk__in=online_friends_sorted_ids)

    if len(friend_suggestions)!=0:
        if len(friend_suggestions) > 1:
            # If there are more than one users other than the current user, shuffle them and take two entries
            friend_suggestions = friend_suggestions.order_by('?')[:2]
        else:
            friend_suggestions = friend_suggestions
    else:
        friend_suggestions = []

    ads =Ad.objects.all().order_by("?")[::2]
    context={'posts':post_obj_final,
    "user":user,
    "post_count":post_count,
    "friend_suggestions":friend_suggestions,
    "online_friends":online_friends_sorted,
    "ads":ads}

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
        resp={'Response':"Error"}
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
def upload_post(request,page):
    user=request.user
    text=request.POST.get('text','')
    image=request.FILES.get('image','')
    video=request.FILES.get('video','')
    share_to=request.POST.get('share_to','')
    image_url=None
    video_url=None
    post_type='Text'
    if image:
        post_type='Image'
        image_resp =publitio_image_upload(bytedata=image,folder_id='jp2rRmM4',title=f"image post by {user.first_name}")
        if image_resp['file_url']:
            if image_resp['file_url'] != 'File upload is not successfull. Please try again':
                image_url = image_resp['file_url']
    elif video:
        post_type='Video'
        video_resp =publitio_video_upload(bytedata=video,folder_id='XGBrb2Wd',title=f"video post by {user.first_name}")
        if video_resp['file_url']:
            if video_resp['file_url'] != 'File upload is not successfull. Please try again':
                video_url = video_resp['file_url']
        
    else:
        post_type='Text'

    post_obj = Post()
    post_obj.user=user
    post_obj.text=text
    # post_obj.feeling=feeling
    post_obj.image=image_url
    post_obj.video=video_url
    if post_type=='Text':
        post_obj.post_type=Post.TEXT
    elif post_type == 'Video':
        post_obj.post_type = Post.VIDEO
    elif post_type == 'Image':
        post_obj.post_type = Post.IMAGE
    post_obj.share_to=Post.PUBLIC
    post_obj.save()

    if page == 'home':
        return redirect('home')
    elif page == 'profile':
        return redirect('profile')



@login_required
def profile(request,id):

    current_user=request.user
    user=User.objects.filter(id=id).first()
    is_current_user=True
    if user!=current_user:
        is_current_user=False

    
    request_obj = Friendship.objects.filter((Q(sender=current_user)&Q(receiver=user))|(Q(sender=user)&Q(receiver=current_user))).first()
    if request_obj:
        if request_obj.status == 'Pending':
            request_status='Pending'
        elif request_obj.status == 'Friends':
            request_status='Friends'
    else:
        request_status='Not Friend'
   

    posts_obj = sorted(Post.objects.filter(user=user), key=lambda x: x.created_at, reverse=True)


    all_friends = set(chain(*Friendship.objects.filter(
            (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
        ).values_list('receiver', 'sender')))
    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    
    friends_count=len(online_friends)

    post_obj_final = list(map(partial(check_post_activity, current_user=user), posts_obj))
    post_count=len(posts_obj)


    context={'posts':post_obj_final,
    "user":user,
    "post_count":post_count,
    "friends_count":friends_count,
    "current_user":current_user,
    "is_current_user":is_current_user,
    "request_status":request_status,
    }

    return render(request,"core/profile.html",context)








@login_required
def saved_posts(request,id):

    current_user=request.user
    user=User.objects.filter(id=id).first()
    is_current_user=True
    if user!=current_user:
        is_current_user=False

    
    request_obj = Friendship.objects.filter((Q(sender=current_user)&Q(receiver=user))|(Q(sender=user)&Q(receiver=current_user))).first()
    if request_obj:
        if request_obj.status == 'Pending':
            request_status='Pending'
        elif request_obj.status == 'Friends':
            request_status='Friends'
    else:
        request_status='Not Friend'
   
    posts =[Post.objects.filter(id=objs).first() for objs in list(chain(*Save.objects.filter(user=user).values_list('post')))]
    print("posts=",posts)
    posts_obj = sorted(posts, key=lambda x: x.created_at, reverse=True)


    all_friends = set(chain(*Friendship.objects.filter(
            (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
        ).values_list('receiver', 'sender')))
    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    
    friends_count=len(online_friends)

    post_obj_final = list(map(partial(check_post_activity, current_user=user), posts_obj))
    post_count=len(posts_obj)


    context={'posts':post_obj_final,
    "user":user,
    "post_count":post_count,
    "friends_count":friends_count,
    "current_user":current_user,
    "is_current_user":is_current_user,
    "request_status":request_status,
    }

    return render(request,"core/saved.html",context)





@login_required
def addfriend(request,receiver):
    sender_obj = request.user
    receiver_obj = User.objects.filter(id=receiver).first()
    friend_obj=Friendship()
    friend_obj.sender=sender_obj
    friend_obj.receiver=receiver_obj
    friend_obj.status='Pending'
    friend_obj.save()
    return redirect(reverse('profile',kwargs={"id":receiver}))






@login_required
def friend_request(request):

   
    user=request.user
   
    all_friends = set(chain(*Friendship.objects.filter(
            (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
        ).values_list('receiver', 'sender')))
    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    
    friends_count=len(online_friends)

    req_obj=Friendship.objects.filter(Q(receiver=user)&Q(status='Pending'))
    req_senders = [friendship.sender for friendship in req_obj]

    print("req",req_senders)
    context={
    "user":user,
    "current_user":user,
    "friends_count":friends_count,
    'friend_requests':req_senders ,
    'is_current_user':True,
    }

    return render(request,"core/friendrequests.html",context)


@login_required
def accept_request(request,sender):

    sender_obj=User.objects.filter(id=sender).first()
    receiver_obj=request.user
    req_obj=Friendship.objects.filter(Q(sender=sender_obj)&Q(receiver=receiver_obj)).first()
    req_obj.status='Friends'
    req_obj.save()

    return redirect('friendrequest')




@login_required
def friends(request,id):

   
    current_user=request.user
    user=User.objects.filter(id=id).first()
    is_current_user=True
    if user!=current_user:
        is_current_user=False
   
    all_friends = set(chain(*Friendship.objects.filter(
            (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
        ).values_list('receiver', 'sender')))
    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    
    friends_count=len(online_friends)




    context={
    "user":user,
    "friends_count":friends_count,
    'current_user':current_user,
    "all_friends":online_friends,
    "is_current_user":is_current_user,
    }

    return render(request,"core/friends.html",context)





@login_required
def unfriend(request,id):

    obj=User.objects.filter(id=id).first()
    obj2=request.user
    req_obj=Friendship.objects.filter((Q(sender=obj)&Q(receiver=obj2))|(Q(sender=obj2)&Q(receiver=obj)))
    if req_obj:
        for item in req_obj:
            item.delete()

    return redirect('friends')




@login_required
def photos(request,id):

    current_user=request.user
    user=User.objects.filter(id=id).first()
    is_current_user=True
    if user!=current_user:
        is_current_user=False

    
    request_obj = Friendship.objects.filter((Q(sender=current_user)&Q(receiver=user))|(Q(sender=user)&Q(receiver=current_user))).first()
    if request_obj:
        if request_obj.status == 'Pending':
            request_status='Pending'
        elif request_obj.status == 'Friends':
            request_status='Friends'
    else:
        request_status='Not Friend'
   

    posts_obj = sorted(Post.objects.filter(Q(user=user)&Q(post_type='Image')), key=lambda x: x.created_at, reverse=True)


    all_friends = set(chain(*Friendship.objects.filter(
            (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
        ).values_list('receiver', 'sender')))
    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    
    friends_count=len(online_friends)

    post_obj_final = list(map(partial(check_post_activity, current_user=user), posts_obj))
    post_count=len(posts_obj)


    context={'posts':post_obj_final,
    "user":user,
    "post_count":post_count,
    "friends_count":friends_count,
    "current_user":current_user,
    "is_current_user":is_current_user,
    "request_status":request_status,
    }

    return render(request,"core/photos.html",context)




@login_required
def videos(request,id):

    current_user=request.user
    user=User.objects.filter(id=id).first()
    is_current_user=True
    if user!=current_user:
        is_current_user=False

    
    request_obj = Friendship.objects.filter((Q(sender=current_user)&Q(receiver=user))|(Q(sender=user)&Q(receiver=current_user))).first()
    if request_obj:
        if request_obj.status == 'Pending':
            request_status='Pending'
        elif request_obj.status == 'Friends':
            request_status='Friends'
    else:
        request_status='Not Friend'
   

    posts_obj = sorted(Post.objects.filter(Q(user=user)&Q(post_type='Video')), key=lambda x: x.created_at, reverse=True)


    all_friends = set(chain(*Friendship.objects.filter(
            (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
        ).values_list('receiver', 'sender')))
    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    
    friends_count=len(online_friends)

    post_obj_final = list(map(partial(check_post_activity, current_user=user), posts_obj))
    post_count=len(posts_obj)

    print("videos-",post_count)
    context={'posts':post_obj_final,
    "user":user,
    "post_count":post_count,
    "friends_count":friends_count,
    "current_user":current_user,
    "is_current_user":is_current_user,
    "request_status":request_status,
    }

    return render(request,"core/videos.html",context)








@login_required
def about(request,id):

   
    current_user=request.user
    user=User.objects.filter(id=id).first()
    is_current_user=True
    if user!=current_user:
        is_current_user=False
   
    all_friends = set(chain(*Friendship.objects.filter(
            (Q(sender=user, status='Friends') | Q(receiver=user, status='Friends'))
        ).values_list('receiver', 'sender')))
    online_friends = [usr for obj in all_friends if (usr := User.objects.filter(id=obj).first()) and usr != user]
    
    friends_count=len(online_friends)




    context={
    "user":user,
    "friends_count":friends_count,
    'current_user':current_user,
    "all_friends":online_friends,
    "is_current_user":is_current_user,
    }

    return render(request,"core/about.html",context)





@login_required
def edit_profile(request,page):

    try:
        pp=request.FILES.get('profilepicture')
        cp=request.FILES.get('coverpicture')
        user=request.user
        image_url1=None
        if pp:
            image_resp =publitio_image_upload(bytedata=pp,folder_id='1J5Bel9l',title=f"profile picture by {user.first_name}")
            if image_resp['file_url']:
                if image_resp['file_url'] != 'File upload is not successfull. Please try again':
                    image_url1 = image_resp['file_url']
        image_url2=None
        if cp:
            image_resp =publitio_image_upload(bytedata=cp,folder_id='kQHy9jLN',title=f"cover picture by {user.first_name}")
            if image_resp['file_url']:
                if image_resp['file_url'] != 'File upload is not successfull. Please try again':
                    image_url2 = image_resp['file_url']

        userprofile = UserProfile.objects.filter(user=user).first()
        if image_url1:
            userprofile.profile_picture=image_url1
        if image_url2:
            userprofile.cover_picture=image_url2
        userprofile.save()
    except:
        messages.error(request, "An Error Occured.")

    if page=="profile":
        return redirect(reverse('profile',kwargs={"id":user.id}))
    elif page == "about":
        return redirect(reverse('about',kwargs={"id":user.id}))
    elif page == "friends":
        return redirect(reverse('friends',kwargs={"id":user.id}))
    elif page == "friendrequest":
        return redirect('friendrequest')
    elif page == 'photos':
        return redirect(reverse('photos',kwargs={"id":user.id}))
    elif page == 'videos':
        return redirect(reverse('videos',kwargs={"id":user.id}))
    else:
        return redirect(reverse('profile',kwargs={"id":user.id}))




@login_required
def save_post(request):
    user=request.user
    request_body= QueryDict(request.body)
    resp={"Response":"Success"}
    try:
        json_data = json.loads(list(request_body.keys())[0]) 
        post_id=json_data.get('post_id')
        save_obj=Save()
        save_obj.user=user
        save_obj.post=Post.objects.filter(id=post_id).first()
        save_obj.save()
    except:
        resp={'Response':"Error"}
    return JsonResponse(resp)



@login_required
def unsave_post(request):
    user=request.user
    request_body= QueryDict(request.body)
    resp={"Response":"Success"}
    try:
        json_data = json.loads(list(request_body.keys())[0]) 
        post_id=json_data.get('post_id')
        save_obj=Save.objects.filter(Q(user=user)&Q(post=Post.objects.filter(id=post_id).first())).first()
        save_obj.delete()
    except:
        resp['Response':"Error"]
    return JsonResponse(resp)


def get_sub_comment_details(comment_id):
    resp=[]
    comments=SubComments.objects.filter(comment=Comment.objects.filter(id=(comment_id)).first())
    if comments:
        for comment in comments:
            dic={}
            dic['comment_id']=comment.id
            dic['comment_text']=comment.comment
            dic['user_id']=comment.user.id
            dic['user_name']=f"{comment.user.first_name} {comment.user.last_name}"
            dic['user_picture']=comment.user.userprofile.profile_picture
            # dic['comment_likes']=SubLike.objects.filter(comment=comment).count
            # dic['sub_comment_details']=get_sub_comment_details(comment_id)
    return resp

def get_comment_details(post_id):
    resp=[]
    comments=Comment.objects.filter(post=Post.objects.filter(id=post_id).first()).order_by('-pk')
    if comments:
        for comment in comments:
            dic={}
            dic['comment_id']=comment.id
            dic['comment_text']=comment.comment
            dic['user_id']=comment.user.id
            dic['user_name']=f"{comment.user.first_name} {comment.user.last_name}"
            dic['user_picture']=comment.user.userprofile.profile_picture
            dic['comment_likes']=SubLike.objects.filter(comment=comment).count()
            dic['commented_date']=comment.created_at
            dic['sub_comment_details']=get_sub_comment_details(comment.id)

            resp.append(dic)
    return resp


def get_post(request):
    current_user=request.user
    request_body= QueryDict(request.body)
    json_data = json.loads(list(request_body.keys())[0]) 
    post_id=json_data.get('post_id')
    post_obj=Post.objects.filter(id=post_id).first()
    like_count=Like.objects.filter(post=post_obj).count()
    comment_count=Comment.objects.filter(post=post_obj).count()
    data={"current_user":{
        "id":current_user.id,
        "image":current_user.userprofile.profile_picture,
        "name":f"{current_user.first_name} {current_user.last_name}",
        
    },
    "posted_user":{
        "id":post_obj.user.id,
        "image":post_obj.user.userprofile.profile_picture,
        "name":f"{post_obj.user.first_name} {post_obj.user.last_name}",
    },
    "post_details":{
        "id":post_id,
        "post_type":post_obj.post_type,
        "post_image":post_obj.image,
        "post_video":post_obj.video,
        "post_text":post_obj.text,
        'post_likes_count':like_count,
        'post_date':post_obj.created_at,
        'comment_count':comment_count,
        "comments":get_comment_details(post_id)
    }}




    resp={"Response":"Success",
          "Details":data}
    print(resp)
    return JsonResponse(resp)






def addcomment(request):
    current_user=request.user
    request_body= QueryDict(request.body)
    json_data = json.loads(list(request_body.keys())[0]) 
    post_id=json_data.get('post_id')
    post_text=json_data.get('post_text')

    comment=Comment()
    comment.user=current_user
    comment.post=Post.objects.filter(id=post_id).first()
    comment.comment=post_text
    comment.save()

    


    resp={"Response":"Success"}
    resp['Details']=get_comment_details(post_id)
    
    return JsonResponse(resp)
