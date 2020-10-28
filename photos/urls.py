from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registration", views.registration, name="registration"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("addpost", views.add_Post, name="add_post"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("like/<int:post_id>", views.like_It, name="like"),
    path("comment/<int:post_id>", views.add_Comment, name="comments"),
    path("delete/<int:post_id>", views.deletePost, name="delete"),
    path("category/<int:category_id>", views.postCategory, name="category"),
    path("myprofile", views.userProfile, name="profile"),
    path('user/<slug:username>', views.user, name="user"),
    path("change/profile/picture", views.changeProfilePicture, name="changeProfilePicture")
]