import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

# Create your models here.

# rename uploaded images
@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename_profiles = PathAndRename("profiles")
path_and_rename_posts = PathAndRename("posts")

class Category(models.Model):
    category_name = models.CharField(max_length=65)

    def __str__(self):
        return f"{self.category_name}"

class Post(models.Model):
    title = models.CharField(max_length=350, default="Untitled")
    img = models.ImageField(upload_to=path_and_rename_posts)
    creator = models.CharField(max_length=65)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.creator}-> ({self.category}) Likes:{self.likes} Date:{self.date} Time:{self.time}"

class UserLikedPost(models.Model):
    user_id = models.IntegerField()
    posts_id = models.IntegerField()

    def __str__(self):
        return f"User: {self.user_id}, Post: {self.posts_id}"

class UserComment(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=250)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=10)
    comment = models.CharField(max_length=250)
    posts_id = models.IntegerField()

    def __str__(self):
        return f"{self.user_id} {self.comment} {self.posts_id}"


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    img = models.ImageField(upload_to=path_and_rename_profiles, blank=True)

    def __str__(self):
        return f"{self.user}"