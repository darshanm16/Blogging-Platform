from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from home.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import AnonymousUser,User
from .serializers import BlogSerializer

# Create your views here.
from django.core.mail import send_mail
from hello.settings import EMAIL_HOST_USER
import random,json
from django.contrib.auth.hashers import make_password


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if entered_otp and session_otp and int(entered_otp) == int(session_otp):
            user_data = json.loads(request.session.get('user'))
            
            user=User.objects.create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                username=user_data['username'],
                email=user_data['email'],
                password=make_password(user_data['password'])
            )
            login(request,user)
            send_welcome_email(user=user)
            messages.success(request, 'Signup successful!')
            return redirect(profile)
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect(verify_otp)
    return render(request,'verify_signup.html')

def verify_signup(request,firstname,lastname,username,email,password):
    otp=random.randint(100000,999999)
    subject = 'Verify your email address'
    message = f"""
Hi {firstname} {lastname},

Welcome to Blogger!

To complete your account registration, please verify your email address by entering the following OTP:
OTP: {otp}

If you didn't create an account with us, please ignore this email.

Happy Blogging,
The Blogger Team

"""
    
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=True,
    )
    
    user_data = {
        'username': username,
        'email': email,
        'first_name': firstname,
        'last_name': lastname,
        'password':password
    }
    request.session['user'] = json.dumps(user_data)

    request.session['otp'] = otp

    # Render the page to prompt the user for OTP input
    return render(request, 'verify_signup.html')
    
def signup(request):
    request.session.flush()
    if request.method=="POST":
        firstname=request.POST.get('fname')
        lastname=request.POST.get('lname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'username or email already exists!')
            return redirect(signup)
        else:
            verify_signup(request, firstname=firstname, lastname=lastname, username=username, email=email, password=password)
            return redirect(verify_otp)
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
        return redirect(login_user)
    
    data=Blogs.objects.exclude(user_name=request.user).values()
    serializer=BlogSerializer(data,many=True)
    d=serializer.data
    
    return render(request,'index.html',{'blogs': d})


def profile(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    
    data=Blogs.objects.filter(user_name=request.user).values()
    serializer=BlogSerializer(data,many=True)
    d=serializer.data

    return render(request,'profile.html',{'blogs': d})


def writeblog(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
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


def send_welcome_email(user):
    subject = 'Welcome to Blogger - Your Account is Ready!'
    message = f"""
Hi {user.first_name},

Welcome to Blogger!

We're excited to have you join our community of bloggers and content creators. Your account has been successfully created, and you're all set to start your blogging journey.

Here are your account details:
- Username: {user.username}
- Email: {user.email}

Get Started:
1. Log in to your account: Click here
2. Set up your profile to introduce yourself to the community.
3. Start writing your first blog post and share your thoughts with the world!

Need help? Check out our Help Center or contact our support team at {EMAIL_HOST_USER}.

We can't wait to see what you'll create!

Happy Blogging,  
The Blogger Team

"""
    
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=True,
    )
