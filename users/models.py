from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from django.conf import settings
from django.utils import timezone



# Create your models here.

class Profile(models.Model):
    # In API
    type='author'
    id= models.CharField(max_length=100, primary_key=True)
    host= models.CharField(max_length=100,default= 'host.default')
    displayName= models.CharField(max_length=100, blank=True, null=True)
    url= models.CharField(max_length=100,blank= True)
    github= models.CharField(max_length=100, blank=True, null=True)    
    profileImage = models.ImageField(default="default.jpg", upload_to="profile_pics")
    
    # Not in API
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name="followed_by", symmetrical= False, blank= True )


    def __str__(self):
        return self.user.username

    # Run after model is saved
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profileImage.path)  # open the current instance
        if img.height > 300 or img.width > 300:
            new_size = (300, 300)
            img.thumbnail(new_size)
            img.save(self.profileImage.path)
            
class Follower(models.Model):
    type='followers'
    items = models.ManyToManyField(Profile, related_name='user_follower')
       
   
class FriendRequest(models.Model):
    type='follow'
    summary= models.CharField(max_length=500, blank= True, null= True)
    actor= models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='actor')
    object= models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='object')
    
class Inbox(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inbox')
    friend_requests = models.ManyToManyField(FriendRequest, related_name='recipient_inboxes')