from django.db import models
from django.contrib.auth.models import User
# Create your models here.




from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="userprofile")
    college = models.CharField(max_length=200)
    college_passed_year = models.IntegerField() 
    highschool = models.CharField(max_length=200)
    highschool_passed_year = models.IntegerField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)  
    SINGLE = 'Single'
    IN_A_RELATIONSHIP = 'In a relationship'
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    ENGAGED='Engaged'
    MALE='Male'
    FEMALE='Female'
    
    RELATIONSHIP_STATUS_CHOICES = [
        (SINGLE, 'Single'),
        (IN_A_RELATIONSHIP, 'In a relationship'),
        (MARRIED, 'Married'),
        (DIVORCED, 'Divorced'),
        (ENGAGED, 'Engaged'),
    ]

    GENDER_CHOICES=[
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    relationship_status = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_STATUS_CHOICES,
        default=SINGLE,
    )
    profile_picture = models.URLField(max_length=500,default='https://media.publit.io/file/echopp/5856.jpg')
    cover_picture = models.URLField(max_length=500,default='https://media.publit.io/file/echocp/defaultcover.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)
    dob=models.DateField()
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default=MALE)
    online=models.BooleanField(default=True)
    

    def __str__(self):
        return self.user.first_name  





class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
    text=models.TextField(null=True,blank=True)
    feeling=models.CharField(max_length=50,null=True,blank=True)
    image=models.URLField(max_length=500,null=True,blank=True)
    video=models.URLField(max_length=500,null=True,blank=True)
    IMAGE='Image'
    VIDEO='Video'
    TEXT='Text'
    POST_TYPE_CHOICES = [
         (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (TEXT, 'Text'),
    ]
    post_type=models.CharField(max_length=20,choices=POST_TYPE_CHOICES,default=TEXT)
    PUBLIC='Public'
    FRIENDS='Friends'
    SHARE_TO_CHOICES = [
         (PUBLIC, 'Public'),
        (FRIENDS, 'Friends'),
    ]
    share_to=models.CharField(max_length=20,choices=SHARE_TO_CHOICES,default=PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Like(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post_likes")
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']



class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post_comments")
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_comments")
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

class SubLike(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name="cpost_ommentlikes")
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_commentlikes")
    comment=models.ForeignKey(User, on_delete=models.CASCADE,related_name="comment_commentlikes")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['comment', 'user']

class SubComments(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post_commentcomments")
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_commentcomments")
    comment=models.ForeignKey(User, on_delete=models.CASCADE,related_name="comment_commentcomments")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)


class Save(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post_saves")
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_saves")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']


class Share(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post_shares")
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_shares")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']



class Friendship(models.Model):
    sender = models.ForeignKey(User, related_name='friendship_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friendship_receiver', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)
    FRIENDS='Friends'
    PENDING='Pending'
    STATUS_CHOICES=[
        (PENDING, 'Pending'),
        (FRIENDS, 'Friends'),
    ]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)

    class Meta:
        unique_together = ['sender', 'receiver']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"



