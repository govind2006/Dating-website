from . import views
# from django.conf.urls import url
from django.contrib.auth.views import (
LoginView,
LogoutView,
PasswordResetView,
PasswordResetDoneView,
PasswordResetConfirmView,
PasswordResetCompleteView,
)
from django.urls import path,include
from django.contrib.auth import views as auth_views

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    # path("chat",include("chat.urls")),

    path('',views.home,name="home"),
    path('load',views.index,name="form"),
    path('form',views.my_form,name="form"),
    path('interested',views.preference_form,name="interested"),
    path('recommendation',views.show,name="interested"),

    path('login',LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout',LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('profile',views.profile,name='profile'),
    path('change_password',views.change_password,name='change_password'),
    path('reset-password', PasswordResetView.as_view(template_name='accounts/reset_password.html'),name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),      

]
#    python -m smtpd -n -c DebuggingServer localhost:1025
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
