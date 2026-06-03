from django.db import models
import uuid
from users.models import Profile

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=240)
    decription = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="projects")
    tags = models.ManyToManyField('Tag', blank=True) # a project can have many tags, tag can have many projects
    featured_image = models.ImageField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio','-vote_ratio']

    def getVotes(self):
        reviews = self.reviews.all()
        upVotes = reviews.filter(value="up").count()
        downVotes = reviews.filter(value="down").count()
        totalVotes = reviews.count()

        if totalVotes != 0:

            voteRatio = (upVotes / totalVotes) * 100
            self.vote_total = totalVotes
            self.vote_ratio = voteRatio
            self.save()
        
        else:
            self.vote_total = 0
            self.vote_ratio = 0
            self.save()






class Review(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=240, choices=[('up', 'Up Vote'), ('down', 'Down Vote')])
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value



class Tag(models.Model):
    name = models.CharField(max_length=240)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name



