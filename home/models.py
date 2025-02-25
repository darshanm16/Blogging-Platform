from django.db import models

# Create your models here.

class Details(models.Model):
    user_name=models.CharField(max_length=100)
    dob=models.DateField(default='2000-01-01')
    role=models.CharField(max_length=100,default='Blogger')
    about=models.TextField(max_length=1000,default='Add about you')
    expertise=models.JSONField(default=list)
    saved=models.JSONField(default=list)
    
    def __str__(self):
        return self.user_name

class Blogs(models.Model):
    user_name=models.CharField(max_length=100)
    title=models.CharField(max_length=100,default='Blog')
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