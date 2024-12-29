from django.urls import path
from home import views

urlpatterns = [
    path("",views.login_user,name="Login"),
    path("signup/",views.signup,name="SignUp"),
    path("index/",views.index,name="Index"),
    path("profile/",views.profile,name="Profile"),
    path("logout/",views.logout_user,name="Profile"),
    path("writeblog/",views.writeblog,name="WriteBlog"),
    path("contact/",views.contact,name="ContactUs")
]