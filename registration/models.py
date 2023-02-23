from django.db import models

# Create your models here.
class EditProfileModel(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    