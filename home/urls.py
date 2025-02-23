from django.urls import path
from home import views

urlpatterns = [
    path("",views.login_user,name="Login"),
    path("sendlink/",views.sendSecuritycode,name="Send_Otp"),
    path("sendlink/verifyotp/",views.codeLogin,name="Verify_Otp"),
    
    path("signup/",views.signup,name="SignUp"),
    path('signup/verifyotp', views.verify_otp, name='VerifyOTP'),
    
    path("index/",views.index,name="Home"),
    path("index/blog/like/",views.updateLikes,name="Likes"),
    path("index/blog/postComment/",views.blogComment,name="Post Comment"),
    path("index/blog/postComment/",views.blogComment,name="Delete Comment"),
    path("index/blog/updateComment/",views.updateComment,name="Edit Comment"),
    path("index/blog/getBlog/",views.getBlog,name="Get Blog"),
    
    path("profile/",views.profile,name="Profile"),
    path("profile/modify-blog/",views.modifyBlog,name="Delete Blog"),
    path("profile/modify-anonymous/",views.updateAnanymous,name="Delete Blog"),
    
    
    path("logout/",views.logout_user,name="Logout"),
    path("writeblog/",views.writeblog,name="WriteBlog"),
    path("contact/",views.contact,name="ContactUs"),
    
]