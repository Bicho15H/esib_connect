from django.contrib import admin
from .models import User,Student,Club,Post

# Register your models here.
class UserView(admin.ModelAdmin):
    list_display = ("id","username", "email","is_student","is_club")
class StudentView(admin.ModelAdmin):
    list_display = ("user",)
class ClubView(admin.ModelAdmin):
    list_display = ("user","is_verified")
class PostView(admin.ModelAdmin):
    list_display = ("id","content","date","user")
admin.site.register(User, UserView)
admin.site.register(Student, StudentView)
admin.site.register(Club, ClubView)
admin.site.register(Post,PostView)