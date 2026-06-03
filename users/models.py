from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=240, blank=True, null=True)
    username = models.CharField(max_length=240, blank=True, null=True)
    email = models.EmailField(max_length=240, blank=True, null=True)
    short_intro = models.CharField(max_length=240, blank=True, null=True)
    bio = models.TextField(max_length=150, blank=True, null=True)
    profile = models.ImageField(null=True, blank=True, upload_to='profiles/', default="images/logo.png")
    social_github = models.CharField(max_length=240, blank=True, null=True)
    social_twitter = models.CharField(max_length=240, blank=True, null=True)
    social_linkedin = models.CharField(max_length=240, blank=True, null=True)
    social_youtube = models.CharField(max_length=240, blank=True, null=True)
    social_website = models.CharField(max_length=240, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
    class Meta:

        ordering = ['created']

class Skills(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="skills")
    name = models.CharField(max_length=240, blank=True, null=True)
    description = models.TextField(max_length=240, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    subject = models.CharField(max_length=240, null=True, blank=True)
    name = models.CharField(max_length=240, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read', '-created']
