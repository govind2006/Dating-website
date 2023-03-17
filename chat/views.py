from django.shortcuts import render, HttpResponse, redirect
from .models import UserProfile, Friends, Messages
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from accounts.views import profile,errormessage
from accounts.models import UploadedImage1

class Person:
  def __init__(self, username, name,img,):
    self.username = username
    self.name = name
    self.img=img

def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = UserProfile.objects.get(username=username)
    id = use.id
    return id

def chatstart(request):
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        dic = list()
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
        for i in friends:
            img=False
            if(UploadedImage1.objects.filter(title=i.username)):
                im = UploadedImage1.objects.get(title=i.username)
                img = im.image
            dic.append(Person(i.username,i.name,img))
        return render(request, "chat/Base.html", {'dic': dic})


def index(request):
    """
    Return the home page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        return profile(request)

def search(request):
    """
    Search users page
    :param request:
    :return:
    """
    users = list(UserProfile.objects.all())
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break
    
    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    dic  = list()
    for i in friends:
        img=False
        if(UploadedImage1.objects.filter(title=i.username)):
            im = UploadedImage1.objects.get(title=i.username)
            img = im.image
        dic.append(Person(i.username,i.name,img))
    
    user_ls = list()
    if request.method == "POST":
        print("SEARCHING!!")
        query = request.POST.get("search").lower()
        if(len(query)!=0):
            query = " ".join(query.split())
            for user in users:
                a = " ".join((user.name).lower().split())
                b = " ".join((user.username).lower().split())
                if query==a or query==b:
                    img = False
                    if(UploadedImage1.objects.filter(title=user.username)):
                        im = UploadedImage1.objects.get(title=user.username)
                        img =  im.image
                    user_ls.append(Person(user.username,user.name,img))
            return render(request, "chat/search.html", {'users': user_ls, 'dic': dic })

    for user in users:
        img = False
        if(UploadedImage1.objects.filter(title=user.username)):
            im = UploadedImage1.objects.get(title=user.username)
            img =  im.image
        user_ls.append(Person(user.username,user.name,img))
    users=user_ls
    return render(request, "chat/search.html", {'users': users, 'dic': dic})


def addFriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """
    
    username = request.user.username
    if not username:
        return errormessage(request,"User is not logged in")
    id = getUserId(username)
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id or name==request.user.username:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("/search")


def removeFriend(request,name):
    username = request.user.username
    id = getUserId(username)
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    c1 = curr_user.friends_set.filter(friend=friend.id)
    c2 = friend.friends_set.filter(friend=id)
    # print(c1,c2)
    c1.delete()
    c2.delete()
    print("Friend Removed!!")
    return redirect("/search")


def chat(request, username):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    friend = UserProfile.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = UserProfile.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        dic  = list()
        for i in friends:
            img=False
            if(UploadedImage1.objects.filter(title=i.username)):
                im = UploadedImage1.objects.get(title=i.username)
                img = im.image
            dic.append(Person(i.username,i.name,img))
        return render(request, "chat/messages.html",
                      {'messages': messages,
                       'dic': dic,
                       'curr_user': curr_user, 'friend': friend})


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)