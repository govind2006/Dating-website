from django.contrib import admin

# Register your models here.
from accounts.models import *

# admin.site.register(UserProfile)
admin.site.register(Show)
admin.site.register(UploadedImage1)
admin.site.register(Preference_show)