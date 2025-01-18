from django.db import models

# Create your models here.

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
    blog_id=models.IntegerField(default=0)
    user_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_name