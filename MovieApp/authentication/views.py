from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from home.views import view_trendings_results, index

# Create your views here.


def register(request):
    if request.method == "POST":
       
       user =  User.objects.create_user(username=request.POST["username"], email=request.POST["email"], password=request.POST["password"])
       login(request, user)   
       return redirect(login_view)
    else:
        return render(request, "authentication/register.html")

def login_view(request):
    if request.method == "POST":
       
       username =request.POST["username"]
       password =request.POST["password"]

       user = authenticate(username=username, password=password) 

       if user is not None:
        login(request, user)
       else:
            return HttpResponse("wrong username or pass") 

       return redirect(index)
    else:
        return render(request, "authentication/login.html")


def logout_view(request):
    return HttpResponse("logged out successfully")

