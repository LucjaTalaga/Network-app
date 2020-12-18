from django.core.paginator import Paginator
from .models import User, Post

def get_posts(page_num, logged_user=None, profile=None):
    # getting all posts (if profile not provided) or all post by profile user and reversing 
    # order to show posts from newest to oldest
    posts =[]
    if profile is None:
        posts_query = Post.objects.all()
        posts = list(reversed(posts_query))
    elif type(profile) is User:
        posts_query = Post.objects.filter(author=profile)
        posts = list(reversed(posts_query))
    else:
        for followed in profile:
            posts_query = Post.objects.filter(author=followed)
            posts += list(reversed(posts_query))
            
    postsPag = Paginator(posts, 10)

    #getting posts per page
    page = postsPag.page(page_num)
    
    # if user is logged in, checking which post she/he liked, counting number of likes per post anyway 
    for post in page:
        if(logged_user):
            is_liked = post.liked_by.filter(username = logged_user).exists()
            post.is_liked = is_liked
        likes = post.liked_by.all()
        post.likes = len(likes)
    
    return page 