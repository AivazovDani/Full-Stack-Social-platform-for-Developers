from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Profile
from projects.models import Tag, Project, Review

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

        fields = ['url', 'username', 'email', 'is_staff']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()


    class Meta:
        model = Project
        fields = '__all__'


