from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from time import localtime, strftime
import re

from .models import Category, Post, UserLikedPost, UserComment, User, ProfilePicture, UserLikedPost

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : None})

    ''' Welcome page '''

    username = User.objects.get(pk=request.user.id)

    context = {
            "user": request.user,
            "categories": Category.objects.all(),
            "posts": Post.objects.all(),
            "profile_picture": ProfilePicture.objects.filter(user=username),
            "slideshow": Post.objects.all()[:3],
        }
    return render(request, 'photos/index.html', context)


def registration(request):

    ''' Registration '''
    
    if request.method == 'GET':    
        logout(request)
        return render(request, "photos/registration.html")
    else:

        firstName = request.POST["first"]
        if not firstName:
            return render(request, "photos/registration.html", {"message": "First name required"})
        lastName = request.POST["last"]
        if not lastName:
            return render(request, "photos/registration.html", {"message": "Last name required"})
        username = request.POST["username"]
        if not username:
            return render(request, "photos/registration.html", {"message": "username required"})
        email = request.POST["email"]
        if not email:
            return render(request, "photos/registration.html", {"message": "Email required"})
        password = request.POST["password"]
        if not password:
            return render(request, "photos/registration.html", {"message": "Password required"})
        if len(password) < 8:
            return render(request, "photos/registration.html", {"message": "Make sure your password have at least 8 letters."})
        elif re.search('[0-9]',password) is None:
            return render(request, "photos/registration.html", {"message": "Make sure your password has a number in it."})
        elif re.search('[A-Z]',password) is None:
            return render(request, "photos/registration.html", {"message": "Make sure your password has a capital letter in it."})
        try:
            user = User.objects.create_user(username, email, password, first_name=firstName, last_name=lastName)
            user.save()
        except IntegrityError:
            return render(request, "photos/registration.html", {"message": "Username Already Taken."})
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    ''' Login '''
    username = request.POST.get("username")
    password = request.POST.get("password")
    if not username and password:
        return render(request, "photos/login.html", {"message": "Invalid Username or Password."})
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "photos/login.html", {"message": "Invalid credentials."})

def add_Post(request):
    ''' Add Post '''
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})

    if request.method == 'GET':

        context = {
            "categories": Category.objects.all(),
            "posts": Post.objects.all(),
        }

        return render(request, 'photos/add_post.html', context)

    else:
        title = request.POST['title']
        if not title:
            return render(request, "photos/error.html", {"message": "Title required"})
        date = strftime(" %a, %d %b %Y", localtime())
        time = strftime(" %I:%M %p", localtime())
        image = request.FILES['img']
        if not image:
            return render(request, "photos/error.html", {"message": "Select an image you want to upload"})
        category_id = request.POST['category']
        category = Category.objects.get(pk=category_id)

        post = Post(title=title, img=image, category=category, date=date, time=time, creator=request.user.username)
        post.save()
        return HttpResponseRedirect(reverse('index'))

def deletePost(request, post_id):
    ''' Delete Post '''

    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})
    try:
        post = Post.objects.get(pk=post_id)
        if post.creator == request.user.username:
            Post.objects.filter(pk=post_id).delete()
            UserLikedPost.objects.filter(posts_id=post_id).delete()
    except Post.DoesNotExist:
        raise Http404("Not Found")
    except UserLikedPost.DoesNotExist:
        raise Http404("Not Found")
    return HttpResponseRedirect(reverse('index'))

def like_It(request, post_id):
    ''' Like Post  '''
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})
    if request.method == 'GET':
        try:
            post = Post.objects.get(pk=post_id)
            liked_post = UserLikedPost.objects.get(user_id=request.user.id, posts_id=post_id)
            if liked_post and post.likes > 0:
                Post.objects.filter(pk=post_id).update(likes=post.likes - 1)
                UserLikedPost.objects.filter(user_id=request.user.id, posts_id=post_id).delete()
                return HttpResponse(post.likes - 1)
        except Post.DoesNotExist:
            raise Http404("Post Not exist")
        except UserLikedPost.DoesNotExist:
            liked = UserLikedPost(user_id=request.user.id, posts_id=post_id)
            Post.objects.filter(pk=post_id).update(likes=post.likes + 1)
            liked.save()
            return HttpResponse(post.likes + 1)
        return HttpResponse(post.likes)
    else:
        return HttpResponse("error")

def post(request, post_id):
    ''' User Post '''
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})
    
    try:
        p = Post.objects.get(pk=post_id)
        u = UserComment.objects.filter(user_id=request.user.id, posts_id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post Not Found")
    except UserComment.DoesNotExist:
        raise Http404("Error while fetching comments")

    context = {
        "user_post": p,
        "user_comments": u,
        "categories": Category.objects.all(),
    }

    try:
        liked_post = UserLikedPost.objects.get(user_id=request.user.id, posts_id=post_id)
    except UserLikedPost.DoesNotExist:
        context.update({'like_status': False})

    return render(request, "photos/post.html", context)


def user(request, username):
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})
    try:
        username = User.objects.get(username=username)
        current_username = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        raise Http404("User Not Exist")

    context = {
        "user": username,
        "profile_picture": ProfilePicture.objects.filter(user=username),
        "user_posts": Post.objects.filter(creator=username),
        "total_posts": Post.objects.filter(creator=username).count(),
        "categories": Category.objects.all(),
    }

    if username == current_username:
        return render(request, "photos/user_profile.html", context)
    else:
        return render(request, "photos/profile.html", context) 

def postCategory(request, category_id):
    ''' Post Category '''
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})

    try:
        category_name = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404("Category not found")

    context = {
        "category": Post.objects.filter(category=category_name),
        "categories": Category.objects.all(),
    }
    return render(request, 'photos/category.html', context)


def add_Comment(request, post_id):

    ''' Add Comment '''
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})

    if request.method == 'POST':
        date = strftime(" %a, %d %b %Y", localtime())
        time = strftime(" %I:%M %p", localtime())
        user_comment = request.POST.get('u_comment')
        if not user_comment:
            raise Http404("Comment Required")
        try:
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            c = UserComment(user_id=user_id, username=user, date=date, time=time, comment=user_comment, posts_id=post_id)
            c.save()
        except UserComment.DoesNotExist:
            raise Http404("Error while commenting try after some time")
        
        object = [
            {"name" : request.user.username, "comment": user_comment, "date": date, "time": time},
        ]

        return JsonResponse(object, safe=False)
    else:
        return HttpResponse("error")


def userProfile(request):
    ''' User Profile '''
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})

    username = User.objects.get(pk=request.user.id)

    context = {
        "user": request.user,
        "profile_picture": ProfilePicture.objects.filter(user=username),
        "user_posts": Post.objects.filter(creator=username),
        "total_posts": Post.objects.filter(creator=username).count(),
        "categories": Category.objects.all(),
    }

    return render(request, "photos/user_profile.html", context)

def changeProfilePicture(request):
    ''' Change Profile Picture '''
    if not request.user.is_authenticated:
        return render(request, "photos/login.html", {"message" : "You Must Login First."})
    
    if request.method == 'POST':
        username = User.objects.get(pk=request.user.id)
        image = request.FILES['image']
        try:
            newPicture = ProfilePicture(user=username, img=image)
            newPicture.save()
        except IntegrityError:
            # delete old profile picture
            ProfilePicture.objects.filter(user=username).delete()
            updatePicture = ProfilePicture(user=username, img=image)
            updatePicture.save()
        return HttpResponseRedirect(reverse('profile'))
    else:
        raise Http404("error")



def logout_view(request):
    ''' Logout '''
    logout(request)
    return render(request, "photos/login.html", {"message": "Logged out."})