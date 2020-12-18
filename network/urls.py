
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.index, {'following': False}, name="following"),
    path("following/<int:following>", views.index, {'following': True}, name="following"),

    # API Routes
    path("add", views.add_post, name="add"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("edit", views.edit, name="edit")    
]
