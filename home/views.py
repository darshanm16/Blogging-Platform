from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from home.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import AnonymousUser,User
from .serializers import BlogSerializer

# Create your views here.

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'username or email already exists!')
            return redirect(signup)

        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        messages.success(request,extra_tags='success', message="User created Successfully!")
        return redirect(signup)
    return render(request,'signup.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect(index)
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(profile)
        else:
            messages.error(request,'Incorrect username or password!')
    return render(request,'login.html')


def logout_user(request):
    logout(request)
    return redirect(login_user)


def index(request):
    if isinstance(request.user, AnonymousUser):
        return HttpResponse("<h1>Your Restricted!</h1>")
    
    data=Blogs.objects.exclude(user_name=request.user).values()
    serializer=BlogSerializer(data,many=True)
    d=serializer.data
    
    return render(request,'index.html',{'blogs': d})


def profile(request):
    if isinstance(request.user, AnonymousUser):
        return HttpResponse("<h1>Your Restricted!</h1>")
    
    data=Blogs.objects.filter(user_name=request.user).values()
    serializer=BlogSerializer(data,many=True)
    d=serializer.data

    return render(request,'profile.html',{'blogs': d})


def writeblog(request):
    if isinstance(request.user, AnonymousUser):
        return HttpResponse("<h1>Your Restricted!</h1>")
    if request.method=="POST":
        user_name =request.user
        title =request.POST.get('title')
        content =request.POST.get('content')  
        
        blog=Blogs(user_name=user_name,title=title,content=content,date=datetime.today())     
        blog.save()
        messages.success(request, "Posted Successfully!")
    
    return render(request,'writeblog.html')

def contact(request):
    return redirect(index)