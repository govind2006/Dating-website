from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid

religion_choices = (
    ('None','None'),
    ('Islam','Islam'),
    ('Hindu', 'Hindu'),
    ('Jain','Jain'),
    ('Christian','Christian'),
    ('Zoroastrianism','Zoroastrianism'),
    ('Sikh','Sikh'),
    ('Buddhist','Buddhist'),
)

gender_choices = (
    ('Other','Other(Both)'),
    ('Male','Male'),
    ('Female','Female'),
)


# Create your models here.
class UploadedImage1(models.Model):
    title = models.CharField(primary_key=True, max_length=150, help_text='Enter an image title')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

class Show(models.Model):
    username = models.CharField( max_length=150,primary_key=True)
    age  = models.FloatField()
    height = models.FloatField()
    Country = models.CharField(max_length=120,blank=True)
    City = models.CharField(max_length=120,blank=True)
    Distance = models.FloatField(max_length=120)
    education = models.CharField(max_length=120,blank=True)
    gender = models.CharField(max_length=6,choices=gender_choices, default='NA')
    religion = models.CharField(max_length=120, choices=religion_choices, default='NA')

class Preference_show(models.Model):
    username = models.CharField('Username', max_length=150,primary_key=True)
    min_height = models.FloatField("Min height",default= None, null=True, blank=True)
    max_height = models.FloatField("Max height",default= None, null=True, blank=True)
    min_age = models.FloatField("Min age",default= None, null=True, blank=True)
    max_age = models.FloatField("Max age",default= None, null=True, blank=True)
    # age_range  = models.CharField('age_range',max_length=7,blank=True)
    # height_range = models.CharField('height_range',max_length=10,blank=True)
    gender = models.CharField('gender',max_length=6,choices=gender_choices, default='NA')
    religion = models.CharField(max_length=120, choices=religion_choices, default='NA')

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default='')
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
#         return f"{self.user}"


# class UserProfile(models.Model):

#     name = models.CharField(max_length=25)
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return f"{self.name}"

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)
