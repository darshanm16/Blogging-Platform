from django.urls import path
from home import views

urlpatterns = [
    path("",views.login_user,name="Login"),
    path("sendlink/",views.sendcode,name="Send_Otp"),
    path("sendlink/verifyotp/",views.resetpassword,name="Verify_Otp"),
    
    path("signup/",views.signup,name="SignUp"),
    path('signup/verifyotp', views.verify_otp, name='VerifyOTP'),
    
    path("index/",views.index,name="Home"),
    path("index/blog/like/",views.updateLikes,name="Likes"),
    
    path("profile/",views.profile,name="Profile"),
    path("profile/modify-blog/",views.modifyBlog,name="Delete Blog"),
    
    
    path("logout/",views.logout_user,name="Logout"),
    path("writeblog/",views.writeblog,name="WriteBlog"),
    path("contact/",views.contact,name="ContactUs"),
    
]