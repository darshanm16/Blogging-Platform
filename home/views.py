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
            Details.objects.create(user_name=request.user)
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


def codeLogin(request):
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
            return redirect(sendSecuritycode) 


def sendSecuritycode(request):
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
                return redirect(sendSecuritycode)
            request.session['resetemail'] = email
            request.session['loginotp'] = loginotp
            
            messages.success(request, 'OTP sent to your email')
    
        else:
            messages.error(request, 'No user found!')
            return redirect(sendSecuritycode)
    return render(request,'sendcode.html')


def logout_user(request):
    request.session.flush()
    logout(request)
    return redirect(login_user)

from django.utils.timesince import timesince

def index(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    
    if request.method=="POST":
        user_name =request.user
        content =request.POST.get('content')  
        blog=Blogs(user_name=user_name,content=content,date=datetime.today())     
        blog.save()
        messages.success(request, "Posted Successfully!")
    
    data=Blogs.objects.exclude(user_name=request.user).values().order_by('-id')
    serializer=BlogSerializer(data,many=True)
    d=serializer.data
    details=Details.objects.filter(user_name=request.user).first()
    saved_blogs = details.saved if details else []
    for blog in d:
        if Likes.objects.filter(blog_id=blog['id'], user_name=request.user).exists():
            blog['liked'] = True
        blog['date'] = datetime.strptime(blog['date'], '%Y-%m-%d').strftime('%b %d, %Y')
        blog['comments'] = Comments.objects.filter(blog_id=blog['id']).order_by('-id')
        blog['no_of_comments'] = len(blog['comments'])
        blog['save']=False
        if blog['id'] in saved_blogs:
            blog['save'] = True
    trending = Blogs.objects.exclude(user_name=request.user).order_by('-likes')[:5]
    
    return render(request,'index.html',{'blogs': d,'trending': trending})

@csrf_exempt
def getBlog(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            blog_id = data.get('id')
            blog = Blogs.objects.get(id=blog_id)
            return JsonResponse({'title': blog.title, 'content': blog.content}, status=200)
        
        except Blogs.DoesNotExist:
            return JsonResponse({'error': 'Blog not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def blogComment(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            blog_id = data.get('id')
            blog_comment = data.get('comment')

            comment = Comments(blog_id=blog_id, user_name=request.user.username, comment=blog_comment)
            comment.save()
            
            total_comments=len(Comments.objects.filter(blog_id=blog_id))
            comment_id=comment.id
            return JsonResponse({'user_name': request.user.username, 'comment': blog_comment,'total_comments':total_comments,'comment_id':comment_id}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            comment_id = data.get('id')
            Comments.objects.filter(id=comment_id).delete()
            return JsonResponse({'message': 'Comment deleted successfully.'}, status=200)
        
        except Blogs.DoesNotExist:
            return JsonResponse({'error': 'Comment not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=400)
            
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

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
            return JsonResponse({'likes':blog.likes,'status':False}, status=200)
        else:
            like = Likes(blog_id=blog_id, user_name=user_name)
            blog = Blogs.objects.get(id=blog_id)
            blog.likes += 1
            blog.save()
            like.save()
            return JsonResponse({'likes':blog.likes,'status':True}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def updateComment(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        comment_id = data.get('id')
        comment_content = data.get('comment')
        comment = Comments.objects.get(id=comment_id)
        comment.comment = comment_content
        comment.save()
        return JsonResponse({'comment': comment.comment}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def saveBlog(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'POST':
        data = json.loads(request.body)
        blog_id = data.get('id')
        blog_id = int(blog_id)
        details = Details.objects.filter(user_name=request.user).first()
        saved_blogs = details.saved
        status = ""
        if blog_id in saved_blogs:
            saved_blogs.remove(blog_id)
            status = "removed"
        else:
            saved_blogs.insert(0,blog_id)
            status = "saved"
        details.saved = saved_blogs
        details.save()
        return JsonResponse({'status': status}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

from django.db.models import Sum

def profile(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    data=Blogs.objects.filter(user_name=request.user).values().order_by('-id')
    total_likes = data.aggregate(Sum('likes'))['likes__sum']
    serializer=BlogSerializer(data,many=True)
    d=serializer.data
    total_comments=0
    for blog in d:
        blog['date'] = datetime.strptime(blog['date'], '%Y-%m-%d').strftime('%b %d, %Y')
        blog['comments'] = Comments.objects.filter(blog_id=blog['id']).order_by('-id')
        blog['no_of_comments'] = len(blog['comments'])
        total_comments+=blog['no_of_comments']
    if str(request.user)=="admin":
        reported_blogs = Blogs.objects.filter(reported__gt=0)
        return render(request,'adminpage.html',{'blogs': d,'total_likes':total_likes,'total_comments':total_comments,'reportedblogs':reported_blogs})
    saved_blogs_id = Details.objects.filter(user_name=request.user).first().saved
    saved_blogs = []
    not_found = []
    for blog_id in saved_blogs_id:
        if not Blogs.objects.filter(id=blog_id).exists():
            not_found.append(blog_id)
            continue
        saved_blogs.append(Blogs.objects.get(id=blog_id))
    if not_found:
        for blog_id in not_found:
            saved_blogs_id.remove(blog_id)
        Details.objects.filter(user_name=request.user).update(saved=saved_blogs_id)
    details=Details.objects.filter(user_name=request.user).first()

    return render(request,'profile.html',{'blogs': d,'total_likes':total_likes,'total_comments':total_comments, 'saved_blogs': saved_blogs,'details':details,'user':request.user})

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
            Likes.objects.filter(blog_id=blog_id).delete()
            Comments.objects.filter(blog_id=blog_id).delete()
            Reports.objects.filter(blog_id=blog_id).delete()
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
        
    if request.method=='PUT':
        data = json.loads(request.body)
        blog_id = data.get('id')
        title = data.get('title')
        content = data.get('content')
        if not blog_id:
            return JsonResponse({'error': 'Blog ID is required.'}, status=400)
        blog = Blogs.objects.get(id=blog_id)
        blog.title = title
        blog.content = content
        blog.save()
        messages.success(request, "Blog updated Successfully!")
        return JsonResponse({'message': 'Blog updated successfully.'}, status=200)

@csrf_exempt
def updateAnanymous(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        blog_id = data.get('id')
        if not blog_id:
            return JsonResponse({'error': 'Blog ID is required.'}, status=400)
        blog = Blogs.objects.get(id=blog_id)
        blog.ananymous = not blog.ananymous
        blog.save()
        return JsonResponse({'ananymous': blog.ananymous}, status=200)

@csrf_exempt
def removeSavedBlog(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'POST':
        data = json.loads(request.body)
        blog_id = data.get('id')
        blog_id = int(blog_id)
        details = Details.objects.filter(user_name=request.user).first()
        saved_blogs = details.saved
        saved_blogs.remove(blog_id)
        details.saved = saved_blogs
        details.save()
        return JsonResponse({'message': 'Blog removed successfully.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def editProfile(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method=="POST":
        if request.POST.get('dob')=="":
            dob=Details.objects.filter(user_name=request.user).first().dob
        else:
            dob=request.POST.get('dob')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        role=request.POST.get('role')
        about=request.POST.get('about')
        
        details = Details.objects.filter(user_name=request.user).first()
        details.dob = dob
        details.role = role
        details.about = about
        details.save()
        
        user = User.objects.get(username=request.user)
        user.first_name = fname
        user.last_name = lname
        user.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect(profile)
    return redirect(profile)

@csrf_exempt
def changeOldPassword(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method=="POST":
        data = json.loads(request.body)
        old_password = data.get('oldpass')
        new_password = data.get('newpass')
        user=User.objects.get(username=request.user)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            login(request,user)
            return JsonResponse({},status=200)
        else:
            return JsonResponse({'message': 'Incorrect old password!'}, status=405)
    return redirect(profile)

@csrf_exempt
def sendResetOtp(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == "POST":
        email = request.user.email
        loginotp = random.randint(100000, 999999)
        subject = 'Your Security Code for Password Reset'
        message = f"""
Dear {request.user.first_name},

Your security code is: {loginotp}

Please use this code to reset your password.

Important Security Tips:
- Do not share this code with anyone.
- If you did not request this code, please contact our support team immediately.

For any assistance, feel free to reach out to us at {EMAIL_HOST_USER}.

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
            return JsonResponse({'status': 'False'}, status=405)
    request.session['loginotp'] = loginotp
    return JsonResponse({'status': 'True'}, status=200)

@csrf_exempt
def verifyResetOtp(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == "POST":
        data = json.loads(request.body)
        form_otp = data.get('otp')
        stored_otp=request.session.get('loginotp')
        if form_otp and stored_otp and int(form_otp) == int(stored_otp):
            del request.session['loginotp']
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({}, status=405)

@csrf_exempt
def changeByOtp(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method=="POST":
        data = json.loads(request.body)
        new_password = data.get('newpass')
        user=User.objects.get(username=request.user)
        user.set_password(new_password)
        user.save()
        login(request,user)
        return JsonResponse({},status=200)
    return redirect(profile)

@csrf_exempt
def blockComments(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'POST':
        data = json.loads(request.body)
        blog_id = data.get('id')
        if not blog_id:
            return JsonResponse({'error': 'Blog ID is required.'}, status=400)
        blog = Blogs.objects.get(id=blog_id)
        blog.blockcomments = not blog.blockcomments
        blog.save()
        return JsonResponse({'blockcomment': blog.blockcomments}, status=200)

@csrf_exempt
def changeStatus(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'POST':
        details = Details.objects.filter(user_name=request.user).first()
        details.public = not details.public
        details.save()
        if details.public:
            return JsonResponse({'status': True}, status=200)
        return JsonResponse({'status': False}, status=200)
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


def ananymousGetSharedblog(request,title,id):
    data=Blogs.objects.get(id=id)
    title=title.replace('_',' ')
    if title != data.title:
        return HttpResponse('Invalid URL!')
    if isinstance(request.user, AnonymousUser):
        return render(request,'sharedBlog.html',{'blog': data })
    else:
        data=Blogs.objects.filter(id=id)
        serializer=BlogSerializer(data,many=True)
        d=serializer.data
        details=Details.objects.filter(user_name=request.user).first()
        saved_blogs = details.saved if details else []
        for blog in d:
            if Likes.objects.filter(blog_id=blog['id'], user_name=request.user).exists():
                blog['liked'] = True
            blog['date'] = datetime.strptime(blog['date'], '%Y-%m-%d').strftime('%b %d, %Y')
            blog['comments'] = Comments.objects.filter(blog_id=blog['id']).order_by('-id')
            blog['no_of_comments'] = len(blog['comments'])
            blog['save']=False
            if blog['id'] in saved_blogs:
                blog['save'] = True
        trending = Blogs.objects.exclude(user_name=request.user).order_by('-likes')[:5]
    
        return render(request,'index.html',{'blogs': d,'trending': trending})
    
def getProfile(request,user_name):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if user_name == request.user.username:
        return redirect(profile)
    if User.objects.filter(username=user_name).exists():
        user=User.objects.get(username=user_name)
        data=Blogs.objects.filter(user_name=user_name).values().order_by('-id')
        total_likes = data.aggregate(Sum('likes'))['likes__sum']
        serializer=BlogSerializer(data,many=True)
        d=serializer.data
        total_comments=0
        for blog in d:
            blog['date'] = datetime.strptime(blog['date'], '%Y-%m-%d').strftime('%b %d, %Y')
            blog['comments'] = Comments.objects.filter(blog_id=blog['id']).order_by('-id')
            blog['no_of_comments'] = len(blog['comments'])
            total_comments+=blog['no_of_comments']
        details=Details.objects.filter(user_name=user).first()
        if not details.public:
            return HttpResponse('User has blocked public access to their profile!')
        return render(request,'profile.html',{'blogs': d,'total_likes':total_likes,'total_comments':total_comments, 'details':details,'user':user})
    return HttpResponse('User not found!')


@csrf_exempt
def reportBlog(request):
    if isinstance(request.user, AnonymousUser):
        return redirect(login_user)
    if request.method == 'POST':
        data = json.loads(request.body)
        blog_id = data.get('blog_id')
        if Reports.objects.filter(blog_id=blog_id,user_id=request.user.id).exists():
            return JsonResponse({'report': True}, status=200)
        Reports.objects.create(blog_id=blog_id, user_id=request.user.id)  
        blog = Blogs.objects.get(id=blog_id)
        blog.reported += 1
        blog.save()        
        return JsonResponse({'report': False}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)