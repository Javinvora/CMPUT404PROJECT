from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from stream.models import TestPost
import uuid
from media.uploads import post_photo
import os

def choose_file_in_folder(post_photo):
    # Get a list of all the files in the folder
    file_list = os.listdir(post_photo)
    
    # Check if there is only one file in the folder
    if len(file_list) == 1:
        # If there is only one file, return it
        return str(os.path.join(post_photo, file_list[0]))
    else:
        # If there are multiple files, raise an error
       return "https://i.imgur.com/default_profile.jpg"


# When a user is saved, send this signal and this reciever (create_profile) takes these arguments and
# instance -> the User instance
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    
    if created:
        profile = Profile.objects.create(user=instance,id=str(uuid.uuid4()))
        profile.id = "host.placeholder/authors/" + str(profile.id) + "/"
        profile.url = "host.placeholder/authors/" + str(profile.id) + "/"
        profile.displayName = instance.username
        profile.github = "https://github.com/" + instance.first_name
        profile.Image=  "https://i.imgur.com/" + choose_file_in_folder(post_photo)
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=User)
def create_post(sender, instance, created, **kwargs):
    if created:
        post = TestPost.objects.create(user=instance,id=str(uuid.uuid4()))
        post.id = "host.placeholder/author/" + profile.id + "/posts/" + str(post.id)
        post.discription = post.content 
        post.author = {
                    "type": "author",
                    "id": profile.id,
                    "url": profile.url,
                    "displayName": profile.displayName,
                    "github": profile.github,
                    "image": profile.image
        }        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()