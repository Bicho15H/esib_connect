from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_student = models.BooleanField(default = False)
    is_club = models.BooleanField(default = False)
    is_admin = models.BooleanField(default=False)
    following = models.ManyToManyField("self",related_name="followers",blank=True,symmetrical=False)
    profile_pic = models.ImageField(blank = True, upload_to = "profile/")

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone = models.CharField(max_length= 30,default="",blank = True)
    campus = models.CharField(max_length=20,default="USJ")
    country = models.CharField(max_length=20,default="",blank = True)
    region = models.CharField(max_length=20,default="",blank = True)
    description = models.TextField(default="",blank = True)

class Club(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=30,default="",blank = True)
    campus = models.CharField(max_length=20,default="USJ",blank = True)
    description = models.TextField(default="",blank = True)

    NOT_VERIFIED = 1
    REQUESTED = 2
    VERIFIED = 3
    VERIFICATION_STATUS = (
        (NOT_VERIFIED,"not_verified"),
        (REQUESTED,"requested"),
        (VERIFIED,"verified")
    )
    is_verified = models.PositiveSmallIntegerField(choices=VERIFICATION_STATUS,default=1)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    image = models.ImageField(blank = True, upload_to = "images/")
    date = models.CharField(max_length=64)
    liked_by = models.ManyToManyField(User,related_name="likes",blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")

    def __str__(self):
        return f"{self.content} -- by {self.user} "
    def __repr__(self):
        return f"{self.content} -- by {self.user} "