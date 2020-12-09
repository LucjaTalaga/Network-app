import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post
from . import utils

def index(request):

    #getting page_num and username and posts per page
    page_num = request.GET.get('page', 1)
    user_name = request.user.username
    if (user_name):
        page = utils.get_posts(page_num, user_name)
    else:
        page = utils.get_posts(page_num)
    
    return render(request, "network/index.html", {
        "posts": page
    })

@login_required(login_url='login')
def add_post(request):

    # adding post must be via "POST" method
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    
    #getting username of logged user and adding new post to database
    user_name = request.user.username
    logged_user = User.objects.get(username=user_name)
    content = json.loads(request.body)
    if content.get("text") is not None:
        new_post = Post(author=logged_user, content=content["text"])
        new_post.save()
        return JsonResponse({"message": "Post added successfully.", "author": user_name, 
        "id": new_post.id }, status=201)

    return JsonResponse({"error": "Post text not found"}, status=404)

@login_required(login_url='login')
def like(request):

    # liking or unliking must be via "POST" or "DELETE" method
    if (request.method != "POST" and request.method != "DELETE"):
        return HttpResponseRedirect(reverse("index"))

    #getting username of logged user and adding or removing liking user from database
    user_name = request.user.username
    logged_user = User.objects.get(username=user_name)
    content = json.loads(request.body)
    id = content.get("id")
    if id is not None:
        post = Post.objects.get(id=id)
        if request.method == "POST":
            post.liked_by.add(logged_user)
        else:
            post.liked_by.remove(logged_user)
        post.save()
        return JsonResponse({"method": request.method}, status=201)

    return JsonResponse({"error": "Post id havent't been found"}, status=404)

@login_required(login_url='login')
def follow(request):

    # following or unfollowing must be via "POST" or "DELETE" method
    if (request.method != "POST" and request.method != "DELETE"):
        return HttpResponseRedirect(reverse("index"))

    #getting username of logged user and adding or removing following from database
    user_name = request.user.username
    logged_user = User.objects.get(username=user_name)
    content = json.loads(request.body)
    id = content.get("id")
    if id is not None:
        profile_user = User.objects.get(id=id)
        if request.method == "POST":
            profile_user.followers.add(logged_user)
        else:
            profile_user.followers.remove(logged_user)
        profile_user.save()
        return JsonResponse({"method": request.method}, status=201)

    return JsonResponse({"error": "User id havent't been found"}, status=404)

def profile(request, id):
    #if id is not supplied, redirect to index page
    if id is None:
        return HttpResponseRedirect(reverse("index"))

    #get user of the profile and logged user, then load the posts
    profile_user = User.objects.get(id=id)
    user_name = request.user.username
    page_num = 1
    if user_name:
        logged_user = User.objects.get(username=user_name)
        page = utils.get_posts(page_num, user_name, profile_user)
    else:
        page = utils.get_posts(page_num=page_num, profile=profile_user)
        logged_user = False

    #getting all followers and people that this profile user follows     
    followers = profile_user.followers.all().count()
    following = User.objects.filter(followers=profile_user).count()
    if (logged_user and (logged_user in profile_user.followers.all())):
        is_followed = True
    else:
        is_followed = False

    return render(request, "network/profile.html", {
        "profile": profile_user,
        "posts": page,
        "followers": followers,
        "following": following,
        "is_followed": is_followed    
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
