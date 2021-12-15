from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.fields import TextField
import datetime as dt

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = CloudinaryField('profile_photos/', default='profile_photos/user')
    name =  models.CharField(max_length =30, blank=True)
    bio = models.TextField(max_length =200, blank=True)
    country = models.CharField(max_length=50)
    email=models.EmailField()
    
  
    def __str__(self):
        return self.user.username
      
    def save_profile(self):
        self.save()
          
    def delete_profile(self):
        self.delete()
        
    @classmethod
    def update_profile(cls,id,profile_pic,name,bio):
        cls.objects.filter(id=id).update(profile_pic=profile_pic,name=name,bio=bio)   
        
    @classmethod
    def get_user(cls,username):
        profile = cls.objects.filter(user__username__icontains=username)
        return profile
    
    
class Projects(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  project_image = CloudinaryField('project_photos/')
  url = models.URLField()
  pub_date = models.DateTimeField(auto_now_add=True)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, related_name="posted_by", on_delete=models.CASCADE, null=True)


  def __str__(self):
    return self.name

  def save_project(self):
    self.save()
  
  def delete_project(self):
    self.delete()

  def voters_num(self):
    return self.voters.count()

  @classmethod
  def get_all_projects(cls):
    return cls.objects.all()

  @classmethod
  def get_project(cls,id):
    return Projects.objects.get(id=id)

  @classmethod
  def search_project(cls,name):
    return cls.objects.filter(name__icontains=name)

  @classmethod
  def user_projects(cls,username):
    return cls.objects.filter(user__username__contains=username)  

class Meta:
  ordering=['-pub_date']
  
  
  
class Rating(models.Model):
    RATINGS = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
  )
  
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Projects, related_name='ratings', on_delete=models.CASCADE, null=True)
    post_date = models.DateTimeField(auto_now_add=True, null=True)
    design = models.FloatField(default=0.00, null=True, choices=RATINGS)
    usability = models.FloatField(default=0.00, null=True, choices=RATINGS)
    content = models.FloatField(default=0.00, null=True, choices=RATINGS)
    
    def __str__(self):
        return self.project.name
      
    class Meta:
        ordering=['-post_date']  

    def save_rating(self):
        self.save()
  
    def delete_rating(self):
        self.delete()
        
        
class Comment(models.Model):
    comment = models.TextField(max_length=2200)
    user = models.ForeignKey(User, related_name='commented_by', on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, related_name='comment_for', on_delete=models.CASCADE)
    pub_date=models.DateField(auto_now_add=True)

    def __str__(self):  
        return self.comment
    
    def save_comment(self):
        self.save()
        
    def delete_comment(self):
        self.delete()      

    @classmethod
    def get_comments(cls,project):
        return cls.objects.filter(project=project)

    
    class Meta:
        ordering=['-pub_date']        
 