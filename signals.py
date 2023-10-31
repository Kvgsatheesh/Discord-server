from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.conf import settings


@receiver(post_save,sender=User)
def user_created(sender,instance,created,**kwargs):
    if created:
        email=instance.email
        send_mail(
            subject=f'welcome.. {instance.username}',
            message= f'welcome to study buddy... ',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]

        )
    
        