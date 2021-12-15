from rest_framework import serializers
from .models import Profile, Projects, Comment, Rating

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'name', 'profile_pic', 'bio', 'country', 'email')
        
        
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'description', 'project_image', 'pub_date', 'profile', 'user')   
        
                   