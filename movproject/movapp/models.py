from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=250)
    img=models.ImageField(upload_to='img',blank=True)
    def __str__(self):
        return self.name

class Addmovie(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    movie_title=models.CharField(max_length=250,unique=True)
    discription=models.TextField()
    poster=models.ImageField(upload_to='poster',blank=True)
    relese_date=models.DateField()
    actor=models.CharField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_title

class ReviewRating(models.Model):
    movie = models.ForeignKey(Addmovie, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject