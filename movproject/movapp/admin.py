from django.contrib import admin
from .models import Addmovie
from .models import Category
from .models import ReviewRating

# Register your models here.
admin.site.register(Addmovie)
admin.site.register(Category)
admin.site.register(ReviewRating)
