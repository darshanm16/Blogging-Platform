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
    path("index/blog/saveblog/",views.saveBlog,name="Save Blog"),
    path("index/blog/report-blog/",views.reportBlog,name="Report Blog"),
    
    path("profile/",views.profile,name="Profile"),
    path("profile/modify-blog/",views.modifyBlog,name="Delete Blog"),
    path("profile/modify-anonymous/",views.updateAnanymous,name="Delete Blog"),
    path("profile/remove-saved-blog/",views.removeSavedBlog,name="Remove Blog"),
    path("profile/editprofile/",views.editProfile,name="Edit Profile"),
    path("profile/change-old-password/",views.changeOldPassword,name="Change Old Password"),
    path("profile/send-reset-otp/",views.sendResetOtp,name="Send Reset Otp"),
    path("profile/verify-reset-otp/",views.verifyResetOtp,name="Verify Reset Password"),
    path("profile/change-by-otp/",views.changeByOtp,name="Change By Otp"),
    path("profile/block-comments/",views.blockComments,name="Block Comments"),
    path("profile/change-status/",views.changeStatus,name="Change Status"),
    
    path("logout/",views.logout_user,name="Logout"),
    path("writeblog/",views.writeblog,name="WriteBlog"),
    
    path("blog/<title>/<int:id>/",views.ananymousGetSharedblog,name="Get shared Blog"),
    path("<user_name>/",views.getProfile,name="Get Profile"),
]