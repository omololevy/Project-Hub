from django.test import TestCase
from .models import Profile, User, Projects, Rating, Comment

# Create your tests here.
class ProfileTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.user = User()
        self.user.save()
        self.profile = Profile(user = self.user, profile_pic = 'photo', name = 'cotech', bio = 'I am the dev', country = 'Kenya', email = 'cotech@gmail.com')
        
    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))
        
    def tearDown(self):
        Profile.objects.all().delete()
    
    # Testing Save Method
    def test_save_method(self):  
        self.profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)
        
    # Testing Update Method    
    def test_update_profile(self):
        self.profile.save_profile()
        self.profile.update_profile(self.profile.id,'photo', 'cotech', 'I am the dev')
        update=Profile.objects.get(profile_pic='photo',name='cotech',bio='I am the dev')
        self.assertEqual(update.bio,'I am the dev')     
 
    # Testing Delete Method  
    def delete_profile(self):
        self.delete() 
        
class ProjectsImageClass(TestCase):
    def setUp(self):
        self.user = User()
        self.user.save()
        self.profile= Profile(user = self.user, profile_pic = 'photo', name = 'cotech', bio = 'I am the dev', country = 'Kenya', email = 'cotech@gmail.com')
        self.profile.save()
        self.project = Projects(name = 'name', description = 'more stories', project_image = 'photo', url = 'url', pub_date = 'date', user = self.user, profile = self.profile)
        
    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.project,Projects)) 
        
    # Testing Save Method
    def test_save_method(self):  
        self.project.save_project()
        projects = Projects.objects.all()
        self.assertTrue(len(projects) > 0)
        
    def tearDown(self):
        Projects.objects.all().delete() 
        Profile.objects.all().delete() 
        User.objects.all().delete()   
      
    def test_delete_project(self):
        self.project.save_project()
        projects = Projects.objects.all()
        self.assertEqual(len(projects),1)
        self.project.delete_project()
        del_project=Projects.objects.all()
        self.assertEqual(len(del_project),0)        
        
        
class CommentTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.user = User()
        self.user.save()
        self.profile= Profile(user = self.user, profile_pic = 'photo', name = 'cotech', bio = 'I am the dev', country = 'Kenya', email = 'cotech@gmail.com')
        self.profile.save()
        self.project = Projects(name = 'project', description = 'more stories', project_image = 'photo', url = 'url', pub_date = 'date', user = self.user, profile = self.profile)
        self.project.save()
        self.comment = Comment(comment = 'what a cool project', user = self.user, project = self.project)
        
    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comment))        

    def tearDown(self):
        User.objects.all().delete() 
        Profile.objects.all().delete()        
        Projects.objects.all().delete() 
        Comment.objects.all().delete() 
           
    # Testing Save Method
    def test_save_method(self):  
        self.comment.save_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) > 0)    
    
    def test_delete_comment(self):
        self.comment.save_comment()
        comments=Comment.objects.all()
        self.assertEqual(len(comments),1)
        self.comment.delete_comment()
        del_comments=Comment.objects.all()
        self.assertEqual(len(del_comments),0)        
        
        
class RatingTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.user = User()
        self.user.save()
        self.profile= Profile(user = self.user, profile_pic = 'photo', name = 'cotech', bio = 'I am the dev', country = 'Kenya', email = 'cotech@gmail.com')
        self.profile.save()
        self.project = Projects(name = 'name', description = 'more stories', project_image = 'photo', url = 'url', pub_date = 'date', user = self.user, profile = self.profile)
        self.project.save()
        self.rating = Rating(user = self.user, project = self.project, post_date = 'date',  design = 0, usability = 0, content = 0)
        
    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.rating,Rating)) 


    def tearDown(self):
        User.objects.all().delete() 
        Profile.objects.all().delete() 
        Projects.objects.all().delete() 
        Rating.objects.all().delete() 

    # Testing Save Method
    def test_save_method(self):  
        self.rating.save_rating()
        ratings = Rating.objects.all()
        self.assertTrue(len(ratings) > 0)    
        
    def test_delete_rating(self):
        self.rating.save_rating()
        ratings=Rating.objects.all()
        self.assertEqual(len(ratings),1)
        self.rating.delete_rating()
        del_rating=Rating.objects.all()
        self.assertEqual(len(del_rating),0)                                          