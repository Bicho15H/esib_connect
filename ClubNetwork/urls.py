from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name = "index"),
    path("login", views.login_view, name="login"),
    path("register", views.register , name = "register"),
    path("register/student", views.register_student, name = "register_student"),
    path("register/club", views.register_club, name = "register_club"),
    path("logout", views.logout_view, name="logout"),
    path("profile/edit",views.edit, name = "edit"),
    path("profile/<int:id>",views.profile, name = "profile"),
    path("newpost", views.newpost, name = "newpost"),
    path("find", views.find_clubs, name = "find"),
    path("request",views.club_request, name = "request"),
    path("search",views.search,name= "search"),
    path("posts/<int:id>", views.posts, name = "posts")
]