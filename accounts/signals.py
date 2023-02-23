from django.db.models.signals import pre_save # Or whatever you are using
from django.dispatch import receiver

from .models import MyModel

@receiver(pre_save, sender=MyModel)
def my_receiver(sender, instance, **kwargs):
    mysender = sender
    print mysender
