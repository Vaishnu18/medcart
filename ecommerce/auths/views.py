from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.forms import ModelForm


def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']                                                            
        confirm_password=request.POST['pass2'] 
        user_type=request.POST.get('user_task')
        if password != confirm_password:
            messages.warning(request,"Password did not match")
            return render(request,'signup.html')
            
        try:
            if User.objects.get(username=email):
                
               messages.info(request,"Email is Taken")
               return render(request,"signup.html")
        except Exception as identifier:
            pass
        user=User.objects.create_user(email,email,password)
        user.is_active=True
        user.user_type=user_type
        user.save()
        messages.info(request,"Account Created")                           
                                   
    return render(request,"signup.html")






def handlelogin(request):
    if request.method=="POST":
        username=request.POST['email']
        password=request.POST['pass']
        myuser=authenticate(username=username, password=password)
        
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auths/login')
    return render(request,"login.html")

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Successful")
    return redirect("/auths/login")

