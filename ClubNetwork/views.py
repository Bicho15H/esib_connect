from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User,Student,Club,Post,Comment

from datetime import datetime

import json

FOLLOWERS_TO_VERIFICATION = 10

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
            return render(request, "ClubNetwork/login.html", {
                "message": "Invalid username and/or password.",
                "data":request.POST
            })
    else:
        return render(request, "ClubNetwork/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    return render(request,"ClubNetwork/register.html")

def register_student(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        message = ""
        if  len(username)< 4:
            message = "Usernames must be at least 4 characters."
        elif len(email) <= 1 or "@" not in email:
            message = "Must enter an email."
        elif len(first_name) ==0 or len(last_name) == 0:
            message = "Must fill in all the fields."
        elif len(password) < 8:
            message = "Password must be at least 8 characters."
        elif password != confirmation:
            message = "Passwords must match."

        if message != "":
            return render(request, "ClubNetwork/register_student.html", {
                "message": message,
                "data":request.POST
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_student = True
            user.save()
            Student(user = user).save()
        except IntegrityError:
            return render(request, "ClubNetwork/register_student.html", {
                "message": "Username already taken.",
                "data": request.POST
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ClubNetwork/register_student.html")

def register_club(request):
    if request.method == "POST":
        club_name = request.POST["club_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        message = ""
        if  len(club_name)< 3:
            message = "Club names must be at least 3 characters."
        elif len(email) <= 1 or "@" not in email:
            message = "Must enter an email."
        elif len(password) < 8:
            message = "Password must be at least 8 characters."
        elif password != confirmation:
            message = "Passwords must match."
        
        if message != "":
            return render(request, "ClubNetwork/register_club.html", {
                "message": message,
                "data":request.POST
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(club_name, email, password)
            user.is_club = True
            user.save()
            Club(user = user).save()
        except IntegrityError:
            return render(request, "ClubNetwork/register_club.html", {
                "message": "Username or club name already taken.",
                "data":request.POST
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"ClubNetwork/register_club.html")

@login_required()
def index(request):
    filter = 'allpost'
    if 'filter' in request.GET:
        if request.GET['filter'] == 'following':
            posts = Post.objects.filter(user__in = request.user.following.all())
            filter = 'following'
        elif request.GET['filter'] == 'notfollowing':
            posts = Post.objects.exclude(user__in = request.user.following.all())
            filter = 'notfollowing'
        elif request.GET['filter'] == 'liked':
            posts = request.user.likes.all()
            filter = 'liked'
        else:
            posts = Post.objects.all()
            filter = 'allpost'
    else:
        posts = Post.objects.all()
    return render(request ,"ClubNetwork/index.html",{
        "posts":posts,
        "filter":filter
    })

@login_required
def edit(request):
    if request.user.is_student:
        if request.method == "POST":
            if request.POST["action"] == "Save Profile":
                email = request.POST["email"]
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                phone = request.POST["phone"]
                campus = request.POST["campus"]
                country = request.POST["country"]
                region = request.POST["region"]
                description = request.POST["description"]
                message = ""
                if len(email) <= 1 or "@" not in email:
                    message = "Must enter an email."
                elif len(first_name) ==0 or len(last_name) == 0:
                    message = "Must fill in all the fields."
                if message != "":
                    return render(request, "ClubNetwork/edit_student.html", {
                        "message": message
                    })
                
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.email = email
                request.user.student.phone = phone
                request.user.student.campus = campus
                request.user.student.country = country
                request.user.student.region = region
                request.user.student.description = description
                request.user.student.save()
                request.user.save()
                return HttpResponseRedirect(reverse("profile",kwargs = {"id" : request.user.id}))
            elif request.POST["action"] == "Unfollow":
                unfollow_target = User.objects.get(pk = request.POST["unfollow_target"])
                request.user.following.remove(unfollow_target)
                return HttpResponseRedirect(reverse("edit"))
            elif request.POST["action"] == "Change profile picture":
                try:
                    profile_pic = request.FILES["image"]
                except:
                    profile_pic = None
                print(profile_pic)
                request.user.profile_pic = profile_pic
                request.user.save()
                return HttpResponseRedirect(reverse("edit"))
        else:
            return render(request,"ClubNetwork/edit_student.html")

    elif request.user.is_club:
        if request.method == "POST":
            if request.POST["action"] == "Save Profile":
                email = request.POST["email"]
                phone = request.POST["phone"]
                campus = request.POST["campus"]
                description = request.POST["description"]
                message =""
                if len(email) <= 1 or "@" not in email:
                    message = "Must enter an email."
                if message != "":
                    return render(request, "ClubNetwork/edit_club.html", {
                        "message": message
                    })
                request.user.email = email
                request.user.club.phone = phone
                request.user.club.campus = campus
                request.user.club.description = description
                request.user.club.save()
                request.user.save()
                return HttpResponseRedirect(reverse("profile",kwargs = {"id" : request.user.id}))
            elif request.POST["action"] == "Unfollow":
                unfollow_target = User.objects.get(pk = request.POST["unfollow_target"])
                request.user.following.remove(unfollow_target)
                return HttpResponseRedirect(reverse("edit"))
            elif request.POST["action"] == "Verify Club":
                if len(request.user.followers.all()) < FOLLOWERS_TO_VERIFICATION:
                    return render(request,"ClubNetwork/edit_club.html",{
                        "message2": "Your request does not match the requirements"
                    })
                else:
                    request.user.club.is_verified = Club.REQUESTED
                    request.user.club.save()
                    return HttpResponseRedirect(reverse("edit"))
            elif request.POST["action"] == "Change profile picture":
                try:
                    profile_pic = request.FILES["image"]
                except:
                    profile_pic = None
                print(profile_pic)
                request.user.profile_pic = profile_pic
                request.user.save()
                return HttpResponseRedirect(reverse("edit"))
        else:
            return render(request,"ClubNetwork/edit_club.html")
    elif request.user.is_admin:
        return HttpResponseRedirect(reverse("index"))  

@login_required
def profile(request, id):
    try:
        target =User.objects.get(pk=id)
    except :
        return HttpResponseRedirect(reverse("index"))
        
    if target.is_student:
        if request.method == "POST":
            if request.POST["action"] == "follow":
                if request.user != target:
                    request.user.following.add(target)
            elif request.POST["action"] == "unfollow":
                if request.user != target:
                    request.user.following.remove(target)
            return HttpResponseRedirect(reverse("profile",kwargs = {"id" : target.id}))
        else:
            if target in request.user.following.all():
                is_following = True
            else:
                is_following = False   
            return render(request,"ClubNetwork/profile_student.html",{
                "target": target,
                "is_following": is_following
            })

    elif target.is_club:
        posts = target.posts.all()
        if request.method == "POST":
            if request.POST["action"] == "follow":
                request.user.following.add(target)
            elif request.POST["action"] == "unfollow":
                request.user.following.remove(target)
            return HttpResponseRedirect(reverse("profile",kwargs = {"id" : target.id}))
        else:
            if target in request.user.following.all():
                is_following = True
            else:
                is_following = False   
            return render(request,"ClubNetwork/profile_club.html",{
                "target": target,
                "posts": posts,
                "is_following": is_following
            })
    elif target.is_admin:
        return HttpResponseRedirect(reverse("index"))

@login_required
def newpost(request):
    if not request.user.is_club:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        if request.user.club.is_verified == Club.VERIFIED:
            content = request.POST["content"]
            date = datetime.now().strftime("%d %B %Y")
            try:
                image = request.FILES["image"]
            except:
                image = None
            if len(content) <=3:
                return render(request,"ClubNetwork/newpost.html",{
                    "message": "Please enter a valid post"
                })
            Post(content = content, date = date,image = image, user = request.user).save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("newpost"))
    else:
        return render(request,"ClubNetwork/newpost.html")

@login_required
def find_clubs(request):
    if request.method == "POST":
        if request.POST["action"] == "follow":
            target = User.objects.get(pk=request.POST["club_target"])
            if target not in request.user.following.all() and target != request.user:
                request.user.following.add(target)
        return HttpResponseRedirect(reverse("find"))
    else:
        return render(request,"ClubNetwork/find.html",{
            "clubs": Club.objects.filter(is_verified__in = [Club.NOT_VERIFIED,Club.REQUESTED]).exclude(description = "")
        })
    
@login_required
def club_request(request):
    if not request.user.is_admin:
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "POST":
        if request.POST["action"] == "accept":
            target = Club.objects.get(pk = request.POST["club_target"])
            if target.is_verified == Club.REQUESTED:
                target.is_verified = Club.VERIFIED
                target.save()
        elif request.POST["action"] == "reject":
            target = Club.objects.get(pk = request.POST["club_target"])
            if target.is_verified == Club.REQUESTED:
                target.is_verified = Club.NOT_VERIFIED
                target.save()
        return HttpResponseRedirect(reverse("request"))
    else:
        return render(request,"ClubNetwork/request.html",{
            "clubs": Club.objects.filter(is_verified = Club.REQUESTED)
        })

@login_required
def search(request):
    try:
        search = request.GET["s"]
    except KeyError:
        search = ""
    result = User.objects.filter(username__icontains=search).exclude(is_admin = True)
    return render(request,"ClubNetwork/search.html",{
        "users":result
    })

@csrf_exempt
@login_required
def posts(request,id):
    try:
        post = Post.objects.get(pk=id)
    except:
        return HttpResponse(status = 404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data["liked"] == True:
            post.liked_by.add(request.user)
        else:
            post.liked_by.remove(request.user)
        return HttpResponse(status=204)
    elif request.method == "GET":
        data = {
            "liked":request.user in post.liked_by.all()
        }
        return JsonResponse(data,safe=False)

@login_required
def post(request,id):
    try:
        post = Post.objects.get(pk=id)
    except:
        return HttpResponse(status = 404)
    if request.method == "POST":
        content = request.POST["content"].strip()
        date = datetime.now().strftime("%d %B %Y")
        if len(content) == 0:
            return HttpResponseRedirect(reverse("post",kwargs = {"id" : post.id}))

        Comment(parent_post = post, content = content, date = date, user = request.user).save()

        return HttpResponseRedirect(reverse("post",kwargs = {"id" : post.id}))
    else:
        return render(request,"ClubNetwork/post.html",{
            "post": post,
            "comments":post.comments.all()
        })