# Esib Connect

### Introduction:
The website goal is to have more exposure to clubs and even create your own club.

### How to run:
First you need to install django if you haven't:
```
pip install django
```

Then in order to run the server on local host, run this command:
```
python manage.py runserver
```

Then open your browser and enter this url: http://127.0.0.1:8000/

### Quick tour around the source code:
##### 1) db.sqlite3
This is where all the data is stored  
We included the database to the source code so the website doesn't feel empty and make it look more crowded (That's why they call it social network 😉 ).  
You can add on top of the data by creating new accounts.  

##### 2)ClubNetwork/
Contain the main application code:  
static/ folder contain mostly css and javascript  
templates/ folder contain all the html files  
models.py file is the logic for the database structure  
urls.py file define all the routes in our website  
views.py file contain the most code and is the center of the application logic  

##### 3)EsibConnect/settings.py
This file contain most of the settings for our project

##### 4)media/
In this folder is stored all the media (photos and profile pictures) of the website

### How to use the website:
When you open the website you can register as a student or as a club. Then you can start messing around and check your profile and edit it.  
If you registered as a student you can like other club posts and follow them.  
If you registered as a club you can do same as the students but also create posts. But in order to create posts you need to have your club verified (need at least X followers). Once you submited a verification request to the admin, you'll have to wait to the admin response.  
Since the website will be running on the localhost there wont be any admin to accept xD. So that's why we will give you the admin account already created on the database so you can try to accept the requests by yourself.  
Username: admin  
Password: admin  

### The team:
Bechara El Helou  
Dani El Hajj  
Marwane Akiki  
Jamal Lahad  
Frank-Germain El Derjany  