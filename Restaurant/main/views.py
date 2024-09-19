from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from datetime import datetime 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.
date=datetime.now().year

@login_required(login_url='login')
def index(request):
    username=request.user.username
    messages.success(request,f"{username}!! Welcome ")
    return render(request, 'index.html',{'date':date})

@login_required(login_url='login')
def contact(request):
    return render(request, 'contact.html',{'date':date})

@login_required(login_url='login')
def about(request):
    return render(request, 'about.html',{'date':date})

@login_required(login_url='login')
def menu(request):
    return render(request, 'menu.html',{'date':date})

@login_required(login_url='login')
def service(request):
    return render(request, 'services.html',{'date':date})

def signin(request):
    if request.method== "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"Incorrect username or password")
            return redirect('login')
        
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Incorrect username or password")

    return render(request,'auth/login.html')

def register(request):
    date=datetime.now()
    if request.method== "POST":
        name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email alreday exists.")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                subject="MOMo Restaurant Registration"
                message=render_to_string('msg.html',{'name':name,'date':date})
                from_email='dahalrohan82@gmail.com'
                recipient_list=[email]
                send_mail(subject,message,from_email,recipient_list,fail_silently=False)
    
                messages.success(request,f"{name} successfully registered")
        else:
            messages.error(request,"Password and Confirm Password does not match")
         
       

        
    return render(request,'auth/register.html')

def log_out(request):
    logout(request)
    return redirect('login')