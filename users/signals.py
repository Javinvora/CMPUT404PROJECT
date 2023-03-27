from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import uuid

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
    
# When a user is saved, send this signal and this reciever (create_profile) takes these arguments and
# instance -> the User instance
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance,id=str(uuid.uuid4()))
        profile.url = "localhost:8000/author/" + str(profile.id) + "/"
        profile.displayName = instance.username
        profile.github = "https://github.com/" + instance.first_name
        
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()