from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from geeks_site import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,"Geeks_app/index.html")

def signup(request):
    if request.method == "POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request,"This username already exists!!!")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,"This email already exists!!!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,"Length of the username must be unser 10 charecters")
        
        if pass1 != pass2:
            messages.error(request,"Pass1 and pass2 mismatch")    
        
        if not username.isalnum():
            messages.error(request,"The username should be Alpha-Numeric")   
            return redirect('home') 
            
            
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        
        messages.success(request,"You account has been succesfully created.We have sent you a confirmation email,please confirm in order to activate your account")
        
        
        # Welcome Email
        subject="Welcome to Geeks_site--Django Login!!!"
        message="Hello"+ myuser.first_name +"!!\n"+" Welcome to Geeks_site \n Thank you for visiting our website \n We have already sent you a confirmation email, please confirm your email in order to activate your account\n\n Thankyou"
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        
        return redirect('signin')
        
    return render(request,"Geeks_app/signup.html")

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        pass1=request.POST['pass1']
        
        user=authenticate(username=username,password=pass1)
        
        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"Geeks_app/index.html",{'fname':fname})
        else:
            messages.error(request,"Bad credentials")
            return redirect('home')
        
            
        
    
    
    return render(request,"Geeks_app/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"You have successfully logged out")
    return redirect('home')
    




    