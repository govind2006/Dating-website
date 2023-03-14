from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *



class UploadImageForm(forms.ModelForm):   
    class Meta: 
        model = UploadedImage1
        fields = ['image', 'title']

class MyForm(forms.ModelForm):
  class Meta:
    model = Show
    fields = ["username", "age","height","Country","City","Distance","education","gender","religion","occuption"]
    labels = {"Age":"age","height":"Height in feet","Country":"Country","City":"City",
    "Distance":"Distance","education":"Education","gender":"Gender","religion":"Religion","occuption":"occuption"}

class PreferenceForm(forms.ModelForm):
  class Meta:
    model = Preference_show
    fields = ["username","min_height","max_height","min_age","max_age","gender","religion"]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
        "username",
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
        )
    def save(self,commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',
        'first_name',
        'last_name',
        'password'
        )
