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
import random
from chat.models import UserProfile, Friends, Messages

def errormessage(request,l):
    return render(request, 'accounts/showdata.html',{'l':l})

class Person1:
  def __init__(self,username, name, img,age,height,gender,country,city,education,religion):
    self.username=username
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
                dic.append(Person1(i.username,name,img,age,height,gender,country,city,education,religion))
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
        lang = (args['intr'].Language).values()
        t = ""
        langsize = len(lang)
        for j in range(0,langsize):
            i = lang[j]
            t = t + i['languages']
            if(j!=langsize-1):
                t = t + ", "
        args['languages'] = t
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
    if request.method == 'POST':
        submitted_form = UploadImageForm(request.POST, request.FILES)
        if submitted_form['title'].value()!=su:
            l = "User not created yet or username is not correct"
            return errormessage(request, l)
        if(UploadedImage1.objects.filter(title=su)):
            image = UploadedImage1.objects.get(title=su)
            image.delete()            
            
        if submitted_form.is_valid():
            submitted_form.save()
        return profile(request)

    form = UploadImageForm()
    context = {
        'form': form,
        'su':su,
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
        form = MyForm(request.POST,request.FILES)
        if(Show.objects.filter(username=su) and form['username'].value()==su):
            val = Show.objects.get(username=su)
            val.delete()
        if form.is_valid() and form['username'].value()==su:
            form.save()
            print("Your preference is submitted successfully...")
            return profile(request)
        else:
            l = "User not created yet or username is not correct"
            return errormessage(request, l)
    else:
        if(Show.objects.filter(username=request.user.username)):
            val = Show.objects.get(username=request.user.username)
            form  = MyForm(instance=val)
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
        form = PreferenceForm(request.POST)
        if(Preference_show.objects.filter(username=su) and form['username'].value()==su):
            val = Preference_show.objects.get(username=su)
            val.delete()
        if form.is_valid() and form['username'].value()==su:
            form.save()
            print("Your preference is submitted successfully...")
            return profile(request)
        else:
            l = "User not created yet or username is not correct"
            return errormessage(request, l)
    else:
        if(Preference_show.objects.filter(username=request.user.username)):
            val = Preference_show.objects.get(username=request.user.username)
            form  = PreferenceForm(instance=val)
        else:
            form = PreferenceForm(instance=request.user)
        return render(request, 'accounts/form.html', {'form': form})

# Recommendation
def falseRecommendation(request):
    l = "Finding your best match..."
    return render(request,'accounts/waitrecommendation.html',{'l':l})

def showRecommendation(request,pk=None):
    if pk:
        user = User.objects.get(pk=pk)
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
        args['Language']=intr.Language
     
    dic = list()
    if(args['interested_data'] or args['prsnl_data']):
        store = matchfunction(args)
        use = UserProfile.objects.get(username=su)
        id = use.id
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        visited = {}
        visited[su]=True
        for i in friends:
            visited[i.username]=True
        for i in store:
            if not i.username in visited:
                visited[i.username]=True
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
                    dic.append(Person1(i.username,name,img,age,height,gender,country,city,education,religion))
    else:
        return home(request)
    print("Total Recommendation = ",len(dic))
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
    print("one sided gender match = ",len(store))

    if given['gender']:
        gendermatch=[]
        for i in store:
            if(Preference_show.objects.filter(username=i.username)):
                intrtwo = Preference_show.objects.get(username=i.username)
                varrel = (intrtwo.gender).lower()
                if(varrel=='male' or varrel=='female'):
                    if(given['gender'].lower()==varrel):
                        gendermatch.append(i)
                else:
                    gendermatch.append(i)
            else:
                gendermatch.append(i)
        store = gendermatch
    print("Two sided gender match = ",len(store))
     
    if given['interested_data']:
        c =given['intr_religion'].lower()
        if c!='na' and c!='none':
            religionmatch=[]
            for i in store:
                if i.religion.lower()==c:
                    religionmatch.append(i)
            store=religionmatch
    print("one sided religion match = ",len(store))

    if given['religion'].lower()!='none' and given['religion'].lower()!='na':
        religionmatch=[]
        for i in store:
            if(Preference_show.objects.filter(username=i.username)):
                intrtwo = Preference_show.objects.get(username=i.username)
                varrel = (intrtwo.religion).lower()
                if(varrel!='na' and varrel!='none'):
                    if(given['religion'].lower()==varrel):
                        religionmatch.append(i)
                else:
                    religionmatch.append(i)
            else:
                religionmatch.append(i)
        store = religionmatch
    print("Two sided religion match = ",len(store))

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
    print("One sided age match = ",len(store))

    if given['age']:
        agematch = []
        for i in store:
            if(Preference_show.objects.filter(username=i.username)):
                intrtwo = Preference_show.objects.get(username=i.username)
                minage = intrtwo.min_age
                maxage = intrtwo.max_age
                if(given['age']>=minage and maxage>=given['age']):
                    agematch.append(i)
            else:
                agematch.append(i)
        store = agematch

    print("Two sided age match = ",len(store))
    
    if given['interested_data']:
        x = given['min_height']
        nx = heightcalculation(chartofloat(x))+int(float(x))*12
        heightmatch = []
        for i in store:
            y = i.height
            ny = heightcalculation(chartofloat(y))+int(float(y))*12
            if ny>=nx:
                heightmatch.append(i)
        store=heightmatch
    if given['interested_data']:
        x = given['max_height']
        nx = heightcalculation(chartofloat(x))+int(float(x))*12
        heightmatch = []
        for i in store:
            y = i.height
            valc = chartofloat(y)
            y1 = float(y)
            ny = heightcalculation(valc)+int(y1)*12
            if nx>=ny:
                heightmatch.append(i)
        store=heightmatch
    print("one sided height match = ",len(store))

    if given['height']:
        hmatch = []
        valc = chartofloat(given['height'])
        x = float(given['height'])
        nx = heightcalculation(valc)+int(x)*12
        for i in store:
            if(Preference_show.objects.filter(username=i.username)):
                intrtwo = Preference_show.objects.get(username=i.username)
                minh = intrtwo.min_height
                maxh = intrtwo.max_height
                nminh = heightcalculation(chartofloat(minh))+int(float(minh))*12
                nmaxh = heightcalculation(chartofloat(maxh))+int(float(maxh))*12
                if(nx>=nminh and nmaxh>=nx):
                    hmatch.append(i)
            else:
                hmatch.append(i)
        store = hmatch
        
    print("Two sided height match = ",len(store))

    if given['Language']:
        lang = given['Language'].values()
        langcheck = set()
        for i in lang:
            langcheck.add(i['languages'])
        langmatch = []
        for i in store:
            if(Preference_show.objects.filter(username=i.username)):
                intr = Preference_show.objects.get(username=i.username)
                lv = intr.Language.values()
                for j in lv:
                    if j['languages'] in langcheck:
                        langmatch.append(i)
                        break
            else:
                langmatch.append(i)
        store = langmatch

    print("Two sided language match = ",len(store))


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
            if(given['Distance']>=x):  #ONE SIDED DISTANCE MATCHING
                if(i.Distance>=x):  #TWO SIDED DISTANCE MATCHING
                    distancematch.append(i)
            store=distancematch
    print("Both sided Distance match = ",len(store))
    total_len = len(store)
    logn_groups = math.ceil(math.log(total_len,2))
    if(logn_groups==0):
        return store
    eachgroup_user = math.ceil(total_len/logn_groups)
    group_data = []
    j,lg=0,0
    result = []
    for i in store:
        group_data.append(i)
        j =j +1
        lg=lg+1
        if(j==eachgroup_user or lg==total_len):
            j=0
            count_result = countminsketch(group_data)
            group_data1 = []
            group_data=group_data1
            r1 = random.randint(0, 3)
            a = r1%4
            b = (r1+1)%4
            for k in count_result:
                if(j==a or j==b):
                    result.append(k)
                j=j+1
            j=0
    return result

def countminsketch(given):
    dic = list()
    rows, cols = (4, 13)
    arr = [[0]*cols]*rows
    idusername = {}
    for i in given:
        su = i.username
        use = UserProfile.objects.get(username=su)
        id = use.id
        idusername[int(id)]=su
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for i in ids:
            num = str(i)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        int_id = int(id)
        h1 = (3*int_id+2)%13
        h2 = (int_id*int_id)%13
        h3 = (int(math.exp(int_id)))%13
        h4 = (int(math.log(int_id,10)))%13
        arr[0][h1] = arr[0][h1]+len(friends)
        arr[1][h2] = arr[1][h2]+len(friends)
        arr[2][h3] = arr[2][h3]+len(friends)
        arr[3][h4] = arr[3][h4]+len(friends)
    top1,top2,top3,top4=0,0,0,0
    i1,i2,i3,i4=False,False,False,False
    for i in idusername:
        int_ids = int(i)
        h1 = (3*int_ids+2)%13
        h2 = (int_ids*int_ids)%13
        h3 = (int(math.exp(int_ids)))%13
        h4 = (int(math.log(int_ids,10)))%13        
        x = min(arr[0][h1],arr[1][h2])
        y = min(arr[2][h3],arr[3][h4])
        x = min(x,y)
        if(x>top1):
            top4=top3
            top3=top2
            top2=top1
            top1=x
            i4=i3
            i3=i2
            i2=i1
            i1=i
        elif(x>top2):
            top4=top3
            top3=top2
            top2=x
            i4=i3
            i3=i2
            i2=i
        elif(x>top3):
            top4=top3
            top3=x
            i4=i3
            i3=i
        elif(x>top4):
            top4=x
            i4=i
    if(i1):
        dic.append(Show.objects.get(username=idusername[i1]))
    if(i2):
        dic.append(Show.objects.get(username=idusername[i2]))
    if(i3):
        dic.append(Show.objects.get(username=idusername[i3]))
    if(i4):
        dic.append(Show.objects.get(username=idusername[i4]))
    return dic


def chartofloat(g):
    valc ="0"
    f = False
    for j in g:
        if(j=='.' or f==True):
            valc = valc + j
            f=True
    return valc

def heightcalculation(p):
    k = str(p)
    if(k=="0.10"):
        return 10
    if(k=="0.11"):
        return 11
    if(k=="0.12"):
        return 12
    return float(p)*10