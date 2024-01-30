
from django.urls import path
from core import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('',views.home,name='home'),
    path('logout/',views.logout_view,name='logoutuser'),
    path('register/',views.registration_view,name='registeruser'),
    path('like-post/',views.like_post,name='likepost'),
    path('dislike-post/',views.dislike_post,name='dislikepost'),
    path('upload-post/<page>/',views.upload_post,name='uploadpost'),
    path('profile/<id>/',views.profile,name='profile'),
    path('addfriend/<receiver>/',views.addfriend,name='addfriend'),
    path('friendrequest/',views.friend_request,name='friendrequest'),
    path('acceptrequest/<sender>/',views.accept_request,name='acceptrequest'),
    path('friends/<id>/',views.friends,name='friends'),
    path('unfriend/<id>/',views.unfriend,name='unfriend'),
    path('photos/<id>/',views.photos,name='photos'),
    path('videos/<id>/',views.videos,name='videos'),
    path('about/<id>/',views.about,name='about'),
    path('edit-profile/<page>/',views.edit_profile,name='editprofile'),
]
