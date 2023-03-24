from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
import uuid

# Create your models here.
class Post(models.Model):
    type="post"
    title = models.CharField(max_length=100)
    content = models.TextField()                               # TextField can have more than 255 characters
    date_posted = models.DateTimeField(default=timezone.now) 
    howManyLike = models.ManyToManyField(User,related_name= "howManyLike")
    image = models.ImageField(upload_to="uploads/post_photo", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # If user is deleted, all his/her posts are deleted
    # we do not need to create an id separately because the Django models create it automiatically.
    source = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    contentType = "text/plain" #default required=True
    categories = models.CharField( max_length=50, blank=True, null=True)
    count = models.IntegerField(default=0)
    comments = models.CharField( max_length=150, blank=True, null=True)
    visibility = models.CharField(max_length=150, blank=True, null=True)
    unlisted = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (
            f"{self.author}"
            f"({self.date_posted:%Y-%m-%d %H:%M}): "
            f"{self.title}"
            f"{self.content}"
            f"{self.image}"
        )    

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def likes(self):
        return self.howManyLike
    


class Comment(models.Model):
    # In API
    type = "comment"
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.TextField(default = "type placeholder")
    published = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # id?
    # Not in API, tentative to change
    main_post = models.ForeignKey(Post, related_name = "main_comments", on_delete=models.CASCADE)

    def __str__(self):
        return '%s  : %s' % (self.main_post.title, self.comment)
    
    def get_absolute_url(self):
        return reverse("stream-home")

class mainlikes(models.Model):
    mainUser = models.ForeignKey(User, on_delete=models.CASCADE)
    mainint = models.CharField(default = "Like", max_length= 5)
    mainPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.mainPost)
    
