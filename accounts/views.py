from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import (
    RegistrationForm,
    EditProfileForm
)
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from .find_dist_btw_cities import *

from geopy.geocoders import Nominatim
from geopy import distance
import math

from chat.models import UserProfile, Friends, Messages

class Person1:
  def __init__(self, name, img,age,height,gender,country,city,education,religion):
    self.name = name
    self.img=img
    self.age = age
    self.height=height
    self.gender=gender
    self.country=country
    self.city=city
    self.education=education
    self.religion=religion

# putting data in the home page
def home(request,pk=None):
    if pk:
        ruser = UserProfile.objects.get(pk=pk)
    else:
        ruser = request.user

        # jab koi request nhi karega
    user = UserProfile.objects.all()
    dic = list()
    
    for i in user:
        if ruser and ruser.username==i.username:
            print(i.username," is Logged IN!!!")
        else:
            name = i.name
            img=False
            age=False
            height=False
            gender=False
            country=False
            city=False
            education=False
            religion=False
            if(Show.objects.filter(username=i.username)):
                j= Show.objects.get(username=i.username)
                age = j.age
                height=j.height
                gender=j.gender
                country = j.Country
                city = j.City
                education = j.education
                religion = j.religion
            if(UploadedImage1.objects.filter(title=i.username)):
                im = UploadedImage1.objects.get(title=i.username)
                img = im.image
            if(name!=" "):
                dic.append(Person1(name,img,age,height,gender,country,city,education,religion))
    return render(request,'accounts/home.html',{'dic':dic})


# showing user profile
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    su = user.username
    args={}
    args['user']=user
    args['name']= UserProfile.objects.get(username=su).name
    if(UploadedImage1.objects.filter(title=su)):
        image = UploadedImage1.objects.get(title=su)
        args['img']=image
    if(Show.objects.filter(username=su)):
        prsnl = Show.objects.get(username=su)
        args['prsnl']=prsnl
    if(Preference_show.objects.filter(username=su)) :
        intr = Preference_show.objects.get(username=su)
        args['intr']=intr    
    return render(request, 'accounts/profile.html', args)



# change user password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

# reset the user password
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})

def PasswordResetCompleteView(request):
    return redirect('/account/login')


# -------------------------------------------------------------


# Upload your profile photo
def index(request,pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    su = user.username
    flag=False
    if(UploadedImage1.objects.filter(title=su)):
        image = UploadedImage1.objects.get(title=su)
        flag=True

    args={}
    args['user']=user

    if request.method == 'POST':
        if(flag):
            image.delete()
        submitted_form = UploadImageForm(request.POST, request.FILES)
        if submitted_form.is_valid():
            submitted_form.save()
            image = UploadedImage1.objects.get(title=su)
            args['img']=image
            if(Show.objects.filter(username=su)):
                prsnl = Show.objects.get(username=su)
                args['prsnl']=prsnl
            if(Preference_show.objects.filter(username=su)):
                intr = Preference_show.objects.get(username=su)
                args['intr']=intr
        return render(request, 'accounts/profile.html', args)

    form = UploadImageForm()
    context = {
        'form': form,
        'su':su,
        # 'images': UploadedImage1.objects.all
    }
    return render(request, 'index.html', context=context)


# fill/edit your personal data
def my_form(request,pk=None):
    if request.method == "POST":
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user
        su = user.username
        flag = False
        if(Show.objects.filter(username=su)):
            val = Show.objects.get(username=su)
            flag = True
        form = MyForm(request.POST,request.FILES)
        if(flag):
            val.delete()
        
        args={}
        args['user']=user
        
        if form.is_valid() and form['username'].value()==user.username:
            form.save()
            prsnl = Show.objects.get(username=su)
            args['prsnl']=prsnl
            if(UploadedImage1.objects.filter(title=user.username)):
                image = UploadedImage1.objects.get(title=user.username)
                args['img']=image
            if(Preference_show.objects.filter(username=su)):
                intr = Preference_show.objects.get(username=su)
                args['intr']=intr
            print("Your form is submitted successfully...")
            return render(request, 'accounts/profile.html', args)
        else:
            val.save()
            print("User not created yet or username is not correct")
            return render(request, 'accounts/profile.html',args)
    else:
        form = MyForm(instance=request.user)
        return render(request, 'accounts/form.html', {'form': form})


# fill/edit your interest
def preference_form(request,pk=None):
    if request.method == "POST":
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user
        su=user.username
        if(Preference_show.objects.filter(username=su)):
            val = Preference_show.objects.get(username=su)
            val.delete()

        args={}
        args['user']=user

        form = PreferenceForm(request.POST)
        if form.is_valid() and form['username'].value()==user.username:
            form.save()

            if(UploadedImage1.objects.filter(title=su)):
                image = UploadedImage1.objects.get(title=su)
                args['img']=image
            if(Show.objects.filter(username=su)):
                prsnl = Show.objects.get(username=su)
                args['prsnl']=prsnl
            intr = Preference_show.objects.get(username=su)
            args['intr']=intr

            print("Your preference is submitted successfully...")
            return render(request, 'accounts/profile.html', args)
        else:
            print("User not created yet or username is not correct")
            return render(request, 'accounts/profile.html',args)
    else:
        form = PreferenceForm(instance=request.user)
        return render(request, 'accounts/form.html', {'form': form})

# Recommendation
def show(request,pk=None):
    flag = False
    if pk:
        user = User.objects.get(pk=pk)
        flag = True
    else:
        user = request.user
    su = user.username
    args={}
    args['username']=su
    args['interested_data']=False
    args['prsnl_data']=False

    if(Show.objects.filter(username=su)):
        prsnl = Show.objects.get(username=su)
        args['prsnl_data']=True
        args['age']=prsnl.age
        args['height']=prsnl.height
        args['gender']=prsnl.gender
        args['Country']=prsnl.Country
        args['City']=prsnl.City
        args['education']=prsnl.education
        args['religion']=prsnl.religion
        args['Distance']=prsnl.Distance
      
    if(Preference_show.objects.filter(username=su)) :
        intr = Preference_show.objects.get(username=su)
        args['interested_data']=True
        args['min_age']=intr.min_age
        args['max_age']=intr.max_age
        args['min_height']=intr.min_height
        args['max_height']=intr.max_height
        args['intr_gender']=intr.gender
        args['intr_religion']=intr.religion
     
    dic = list()
    if(args['interested_data'] or args['prsnl_data']):
        store = matchfunction(args)
        for i in store:
            if i.username!=su:
                j = UserProfile.objects.get(username=i.username)
                name = j.name
                img=False
                age = i.age
                height=i.height
                gender=i.gender
                country = i.Country
                city = i.City
                education = i.education
                religion = i.religion
                if(UploadedImage1.objects.filter(title=i.username)):
                    im = UploadedImage1.objects.get(title=i.username)
                    img = im.image
                if(name!=" "):
                    dic.append(Person1(name,img,age,height,gender,country,city,education,religion))
    else:
        return home(request)
    return render(request,'accounts/recommendation.html',{'dic':dic})


def matchfunction(given):
    store = Show.objects.all()
    if given['interested_data']:
        if (given['intr_gender'].lower()=='male' or given['intr_gender'].lower()=='female'):
            gendermatch=[]
            for i in store:
                if given['intr_gender'].lower()==i.gender.lower():
                    gendermatch.append(i)
            store=gendermatch
    print(" 1 = ",len(store))
    if given['interested_data']:
        c =given['intr_religion'].lower()
        if c!='na' and c!='none':
            religionmatch=[]
            for i in store:
                if i.religion.lower()==c:
                    religionmatch.append(i)
            store=religionmatch
    print(" 2 = ",len(store))
    if given['interested_data']:
        x = given['min_age']
        agematch = []
        for i in store:
            if i.age>=x:
                agematch.append(i)
        store=agematch
    if given['interested_data']:
        x = given['max_age']
        agematch = []
        for i in store:
            if i.age<=x:
                agematch.append(i)
        store=agematch
    print(" 3 = ",len(store))
    if given['interested_data']:
        x = given['min_height']
        heightmatch = []
        for i in store:
            if i.height>=x:
                heightmatch.append(i)
        store=heightmatch
    if given['interested_data']:
        x = given['max_height']
        heightmatch = []
        for i in store:
            if x>=i.height:
                heightmatch.append(i)
        store=heightmatch
    print(" 4 = ",len(store))
    if given['City'] and given['Country'] and given['Distance']:
        distancematch = []
        c1 = given['City']+" "+given['Country']
        geolocater  = Nominatim(user_agent="geoapiExercises")
        l1 = geolocater.geocode(c1,timeout=None)
        loc1 = (l1.latitude,l1.longitude)
        for i in store:
            c2 = i.City+" "+i.Country
            l2 = geolocater.geocode(c2,timeout=None)
            loc2 = (l2.latitude,l2.longitude)
            x = math.ceil(distance.distance(loc1,loc2).km)
            if(given['Distance']>=x):
                distancematch.append(i)
            store=distancematch
    print(" 5 = ",len(store))
    return store

# https://en.wikipedia.org/wiki/List_of_cities_in_West_Bengal_by_population
# https://en.wikipedia.org/wiki/List_of_cities_in_Bihar_by_population