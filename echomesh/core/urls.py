



from django.urls import path
from core import views

urlpatterns = [
    path('',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout_view,name='logoutuser'),
    path('register/',views.registration_view,name='registeruser'),
    path('like-post/',views.like_post,name='likepost'),
    path('dislike-post/',views.dislike_post,name='dislikepost'),
    path('upload-post/',views.upload_post,name='uploadpost'),
]
