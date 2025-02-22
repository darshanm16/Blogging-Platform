from django.db import models

# Create your models here.

class Userdetails(models.Model):
    dob=models.DateField()
    role=models.CharField(max_length=100)
    about=models.TextField(max_length=1000)
    expertise=models.JSONField(default=list)

class Blogs(models.Model):
    user_name=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    content =models.TextField(max_length=10000)
    date =models.DateField()
    ananymous=models.BooleanField(default=False)
    likes=models.IntegerField(default=0)
    
    def __str__(self):
        return self.user_name
    
class Likes(models.Model):
    blog_id=models.IntegerField()
    user_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_name
    
class Comments(models.Model):
    blog_id=models.IntegerField()
    user_name=models.CharField(max_length=100)
    comment=models.TextField(max_length=1000)
    
    def __str__(self):
        return self.user_name