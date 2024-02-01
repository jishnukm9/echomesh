from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SubLike)
admin.site.register(SubComments)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Share)
admin.site.register(Friendship)
admin.site.register(Ad)


