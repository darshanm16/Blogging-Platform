from django.db import models

# Create your models here.

class Blogs(models.Model):
    user_name=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    content =models.TextField(max_length=10000)
    date =models.DateField()
    
    def __str__(self):
        return self.user_name