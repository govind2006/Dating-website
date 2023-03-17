from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate
from chat.models import UserProfile
from django.contrib.auth.models import User

def EditProfile(request):
    username = request.user.username
    if request.method =="POST":
        form = EditProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            givenusername = form.cleaned_data.get('username')
            profile_form = UserProfile.objects.get(username=username)
            allvalue = UserProfile.objects.all()
            for i in allvalue:
                if(i.email==email and i.username!=username):
                    l = "Email already registered with other username"
                    return render(request,'accounts/showdata.html',{'l':l})
            x = User.objects.get(username=username)
            x.username=givenusername
            x.email = email
            x.first_name=name
            x.save()
            profile_form.username=givenusername
            profile_form.name = name
            profile_form.email = email
            profile_form.save()
            if(username==givenusername):
                return redirect('/account/profile')
            return redirect("/")

    else:
        if(UserProfile.objects.filter(username=request.user.username)):
            val = UserProfile.objects.get(username=request.user.username)
            form  = EditProfileForm(instance=val)
        else:
            form = EditProfileForm(instance=request.user)
    return render(request, "registration/signup.html", {"form": form})

def SignUp(request):
    message = []
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.validate_email()
            username = form.validate_username()
            password = form.validate_password()
            if not email:
                # message.append("Email already registered!")
                l="Email already registered!"
                return render(request,'accounts/showdata.html',{'l':l})
            elif not password:
                l="Passwords don't match!"
                return render(request,'accounts/showdata.html',{'l':l})
            elif not username:
                l="Username already registered!"
                return render(request,'accounts/showdata.html',{'l':l})
            else:
                print(username," is successfully registered!!!")
                form.save()
                profile = UserProfile(email=email, name=name, username=username)
                profile.save()
                x = User.objects.get(username=username)
                x.first_name = name
                x.save()
                return redirect("/login")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form, "heading": "Sign Up", "message": message})