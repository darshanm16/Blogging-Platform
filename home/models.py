from django.db import models

# Create your models here.

class Details(models.Model):
    user_name=models.CharField(max_length=100)
    dob=models.DateField(default='2000-01-01')
    role=models.CharField(max_length=100,default='Set your role')
    about=models.TextField(max_length=1000,default='Tell me about yourself...')
    badges=models.JSONField(default=list)
    saved=models.JSONField(default=list)
    public=models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_name

class Blogs(models.Model):
    user_name=models.CharField(max_length=100)
    title=models.CharField(max_length=100,default='Blog')
    content =models.TextField(max_length=10000)
    date =models.DateField()
    ananymous=models.BooleanField(default=False)
    likes=models.IntegerField(default=0)
    blockcomments=models.BooleanField(default=False)
    reported=models.IntegerField(default=0)
  
    def __str__(self):
        return self.user_name

class Reports(models.Model):
    blog_id=models.ImageField()
    user_id=models.IntegerField()

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