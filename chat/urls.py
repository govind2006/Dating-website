from django.urls import path, include
from . import views
from django.contrib.auth.views import (
LoginView,
LogoutView,
PasswordResetView,
PasswordResetDoneView,
PasswordResetConfirmView,
PasswordResetCompleteView,
)
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path("", views.index, name="index"),
    path("chatstart/",views.chatstart, name="chatstart"),
    path("search/", views.search, name="search"),
    path("addfriend/<str:name>", views.addFriend, name="addFriend"),
    path("removefriend/<str:name>", views.removeFriend, name="removeFriend"),
    path("chat/<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)