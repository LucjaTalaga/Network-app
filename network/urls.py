
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),

    # API Routes
    path("add", views.add_post, name="add"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow")
]
