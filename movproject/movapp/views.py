from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Addmovie,Category,ReviewRating
from .forms import movForm,Rivewform
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages, auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='movapp:login')
def movie(request):
    category = request.GET.get('category')
    if category == None:
        usermovie = Addmovie.objects.order_by('relese_date')
    else:
        usermovie = Addmovie.objects.filter(category__name=category)

    page_num = request.GET.get("page")
    paginator = Paginator(usermovie, 3)
    try:
        usermovie = paginator.page(page_num)
    except PageNotAnInteger:
        usermovie = paginator.page(1)
    except EmptyPage:
        usermovie = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    context={
        'usermovie':usermovie,
        'categories': categories
    }

    return render(request,'index.html',context)
@login_required(login_url='movapp:login')
def modal(request):

    return render(request,'index.html')
@login_required(login_url='movapp:login')
def detail(request,movie_id):
    movie = Addmovie.objects.get(id=movie_id)
    return render(request,'shop-single.html',{'movie':movie})
@login_required(login_url='movapp:login')
def addMovie(request):
    form = movForm()
    if request.method=="POST":
        form =movForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=movForm()
    context={
        'form':form
        }

    return render(request,'add.html',context)

@login_required(login_url='movapp:login')
def delete(request,id):
    if request.method=='POST':
        move=Addmovie.objects.get(id=id)
        move.delete()
        return redirect('/')
    return render(request,'delete.html')

@login_required(login_url='movapp:login')
def update(request,id):
    movie=Addmovie.objects.get(id=id)
    form=movForm(request.POST or None, request.FILES,instance=movie)
    if  form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'form':form,'movie':movie})


def register(request):
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['password1']
            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username taken")
                    return redirect('movapp:register')
                if User.objects.filter(email=email).exists():
                    messages.info(request, "email taken")
                    return redirect('movapp:register')
                else:
                    user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                    last_name=last_name, email=email)
                    user.save()
                    return redirect('movapp:login')
            else:
                messages.info(request, "Password not matching")
                return redirect('register')
        return render(request, "register.html")

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credentials")
            return redirect('login')

    return render(request,'login.html',)

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='movapp:login')
def searchBar(request):
    usermovie=None
    query=None
    if'q' in request.GET:
        query=request.GET.get('q')
        usermovie=Addmovie.objects.all().filter(Q(movie_title__icontains=query)|Q(discription__contains=query))
    return render(request,'searchbar.html', {'query':query,'usermovie' : usermovie})

@login_required(login_url='movapp:login')
def profile(request,user_name):
    user_related_data=Addmovie.objects.filter(posted_by__username=user_name)
    context={
        'user_related_data':user_related_data
    }
    return render(request,'profile.html',context)

@login_required(login_url='movapp:login')
def submit_review(request,movie_id):
    if request.method=='POST':
        url=request.META.get('HTTP_REFERER')
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,movie__id=movie_id)
            form = Rivewform(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form=Rivewform(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.movie_id=movie_id
                data.user_id=request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


def commends(request):
    commends = ReviewRating.objects.all()
    context = {
        'commends': commends
    }
    return render(request,'commends.html',context)