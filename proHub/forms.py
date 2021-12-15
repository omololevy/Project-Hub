from django import forms
from .models import Profile, Projects, Rating

class CreateProfileForm(forms.ModelForm):  
    class Meta:
        model = Profile
        exclude = ['user']
        
        
class NewSiteForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['profile', 'user', 'pub_date', 'voters']
        
        
class RatingForm(forms.ModelForm):
  class Meta:
    model = Rating
    fields = ['design', 'usability', 'content']    
    
    
class UpdateProfile(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['profile_pic', 'name', 'bio', 'country', 'email']        
                