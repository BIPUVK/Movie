from django import forms
from .models import Addmovie,ReviewRating

class DateInput(forms.DateInput):
    input_type = 'date'

class movForm(forms.ModelForm):
    class Meta:
        model=Addmovie
        fields=['posted_by','movie_title','poster','category','discription','relese_date','actor']
        widgets={
            'posted_by': forms.Select(attrs={'class': 'form-control'}),
            'movie_title':forms.TextInput(attrs={'class':'form-control'}),
            'discription': forms.TextInput(attrs={'class': 'form-control'}),
            'poster':forms.FileInput(attrs={'class':'form-control','type':'file'}),
            'relese_date': DateInput(),
            'actor': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class Rivewform(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['subject','review','rating']