from django.db import models
import datetime
import time


# Create your models here.
class Users(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    passwd = models.CharField(max_length=50)
    head_img = models.ImageField(upload_to='headimg')
    admin = models.IntegerField(default=0)
    created_at = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Blogs(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64)
    user_name = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='blogimg')
    title = models.CharField(max_length=50)
    content = models.TextField()
    abstract = models.TextField()
    created_at = models.FloatField(default=0.0)
    def __str__(self):
        return self.title


class Comments(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    blog_id = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
    user_name = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='commentimg')
    content = models.TextField()
    created_at = models.FloatField(default=0.0)

    def __str__(self):
        return self.blog_id
