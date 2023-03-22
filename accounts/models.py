from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
from accounts.occuption import occuption_choices
from accounts.languages import language_choices
from multiselectfield import MultiSelectField

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

education_choices = (
    ('10th','10th'),
    ('12th','12th'),
    ('Diploma','Diploma'),
    ('B.Tech','B.Tech'),
    ('M.Tech','M.Tech'),
    ('PHD','PHD'),
    ('Post Doctorate','Post Doctorate'),
)

class UploadedImage1(models.Model):
    title = models.CharField(primary_key=True, max_length=150, help_text='Enter an image title')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

class Show(models.Model):
    username = models.CharField( max_length=150,primary_key=True)
    age  = models.FloatField()
    height = models.CharField(max_length=120)
    Country = models.CharField(max_length=120,blank=True)
    City = models.CharField(max_length=120,blank=True)
    Distance = models.FloatField(max_length=120)
    education = models.CharField(max_length=120,choices=education_choices, default='NA')
    gender = models.CharField(max_length=6,choices=gender_choices, default='NA')
    religion = models.CharField(max_length=120, choices=religion_choices, default='NA')
    occuption = models.CharField(max_length=120, choices=occuption_choices, default='NA') 
    def __str__(self):
        return self.username

class alllang(models.Model):
    languages = models.CharField(max_length=120, choices=language_choices, default='NA')

    def __str__(self):
        return self.languages

class Preference_show(models.Model):
    username = models.CharField('Username', max_length=150,primary_key=True)
    min_height = models.FloatField("Min height",default= None, null=True, blank=True)
    max_height = models.FloatField("Max height",default= None, null=True, blank=True)
    min_age = models.FloatField("Min age",default= None, null=True, blank=True)
    max_age = models.FloatField("Max age",default= None, null=True, blank=True)
    gender = models.CharField('gender',max_length=6,choices=gender_choices, default='NA')
    religion = models.CharField(max_length=120, choices=religion_choices, default='NA')
    Hobbies = models.CharField(max_length=120,blank=True)
    Language = models.ManyToManyField(alllang,max_length=120)
    # Language = MultiSelectField(max_length=120, choices=language_choices, default='NA')

    def __str__(self):
        return self.username
