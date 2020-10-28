from django.contrib import admin

# Register your models here.

from . models import Category, Post, UserLikedPost, UserComment, ProfilePicture

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(UserLikedPost)
admin.site.register(UserComment)
admin.site.register(ProfilePicture)