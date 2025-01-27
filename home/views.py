from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from home.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import AnonymousUser,User
from .serializers import BlogSerializer
from django.core.mail import send_mail
from hello.settings import EMAIL_HOST_USER
import random,json
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt


def resetpassword(request):
    if request.method == "POST":
        form_otp=request.POST.get('formotp')
        stored_otp=request.session.get('loginotp')
        if form_otp and stored_otp and int(form_otp) == int(stored_otp):
            user=User.objects.get(email=request.session.get('resetemail'))
            login(request,user)
            del request.session['loginotp']
            del request.session['resetemail']
            return redirect(profile)
        else:
            messages.error(request, 'Invalid OTP! Please try again.')
            return redirect(sendcode) 

def sendcode(request):
    if request.method == "POST":
        email = request.POST.get('resetEmail')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            loginotp = random.randint(100000, 999999)
            subject = 'Your Security Code for Login'
            message = f"""
Dear {user.first_name},

Your security code is: {loginotp}

Please use this code to complete your login process.

Important Security Tips:
-Do not share this code with anyone.
-If you did not request this code, please contact our support team immediately.

For any assistance, feel free to reach out to us at {EMAIL_HOST_USER} or {9482216949}.

Thank you,
The Blogger Team

"""
            if not send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [email],
                fail_silently=True,
            ):
                messages.error(request, 'There was an error sending the email. Please try again later.')
                return redirect(sendcode)
            request.session['resetemail'] = email
            request.session['loginotp'] = loginotp
            
            messages.success(request, 'OTP sent to your email')
    
        else:
            messages.error(request, 'No user found!')
            return redirect(sendcode)
    return render(request,'sendcode.html')
    

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
            messages.success(request, 'Signup successful! check your mail for confirmation')
            return redirect(profile)
        else:
            messages.error(request, 'Invalid OTP! Please try again.')
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
    
    if send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=True,
    ):
        user_data = {
            'username': username,
            'email': email,
            'first_name': firstname,
            'last_name': lastname,
            'password':password
        }
        request.session['user'] = json.dumps(user_data)
        request.session['otp'] = otp
        return True
    else:
        messages.error(request,"Verification failed. Kindly retry in a moment.")
        return False
    
    
def signup(request):
    request.session.flush()
    if request.method=="POST":
        firstname=request.POST.get('fname')
        lastname=request.POST.get('lname')
        email=request.POST.get('email')
        key=email.index('@')
        username=email[:key]
        password=request.POST.get('password')
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'username or email already exists!')
            return redirect(signup)
        else:
            if verify_signup(request, firstname=firstname, lastname=lastname, username=username, email=email, password=password):
                return redirect(verify_otp)
            else:
                return redirect(signup)
    return render(request,'signup.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect(index)
    
    if request.method=="POST":
        username=request.POST.get('username')
        if '@' in username:
            key=username.index('@')
            username=username[:key]
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(profile)
        elif not User.objects.filter(username=username).exists():  
            messages.error(request,'User not registered!')
        else:
            messages.error(request,'Incorrect password!')
    return render(request,'login.html')


def logout_user(request):
    request.session.flush()
    logout(request)
    return redirect(login_user)


def index(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    
    data=Blogs.objects.exclude(user_name=request.user).order_by('?').values()
    serializer=BlogSerializer(data,many=True)
    d=serializer.data
    return render(request,'index.html',{'blogs': d})


@csrf_exempt
def updateLikes(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        blog_id = data.get('id')
        user_name = request.user
        if Likes.objects.filter(blog_id=blog_id, user_name=user_name).exists():
            Likes.objects.filter(blog_id=blog_id, user_name=user_name).delete()
            blog = Blogs.objects.get(id=blog_id)
            blog.likes -= 1
            blog.save()
            return JsonResponse({'likes':blog.likes}, status=200)
        else:
            like = Likes(blog_id=blog_id, user_name=user_name)
            blog = Blogs.objects.get(id=blog_id)
            blog.likes += 1
            blog.save()
            like.save()
            return JsonResponse({'likes':blog.likes}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def profile(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    data=Blogs.objects.filter(user_name=request.user).values()
    serializer=BlogSerializer(data,many=True)
    d=serializer.data
    
    if str(request.user)=="admin":
        return render(request,'adminpage.html',{'blogs': d})

    return render(request,'profile.html',{'blogs': d})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def modifyBlog(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            blog_id = data.get('id')
            if not blog_id:
                return JsonResponse({'error': 'Blog ID is required.'}, status=400)
            blog = Blogs.objects.get(id=blog_id)
            blog.delete()
            messages.success(request, "Blog deleted Successfully!")
            return JsonResponse({'message': 'Blog deleted successfully.'}, status=200)
        
        except Blogs.DoesNotExist:
            return JsonResponse({'error': 'Blog not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=400)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            blog_id = data.get('id')
            title = data.get('title')
            content = data.get('content')

            blog = Blogs.objects.get(id=blog_id)
            blog.title = title
            blog.content = content
            blog.save()
            messages.success(request, "Blog updated Successfully!")
            return JsonResponse({'message': 'Blog updated successfully.'}, status=200)
        
        except Blogs.DoesNotExist:
            return JsonResponse({'error': 'Blog not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=400)


    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def writeblog(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method=="POST":
        user_name =request.user
        title =request.POST.get('title')
        content =request.POST.get('content')  
        check =request.POST.get('ananymous')  
        if check=='True':
            blog=Blogs(user_name=user_name,title=title,content=content,date=datetime.today(),ananymous=True)     
            blog.save()
            messages.success(request, "Posted Successfully!")
            return redirect(writeblog)
        blog=Blogs(user_name=user_name,title=title,content=content,date=datetime.today())     
        blog.save()
        messages.success(request, "Posted Successfully!")
    
    return render(request,'writeblog.html')

def contact(request):
    return render(request,'contact.html')


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
