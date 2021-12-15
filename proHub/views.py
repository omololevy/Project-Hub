from django.contrib.auth.models import User
from django.core import exceptions
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import CreateProfileForm
from django.http import HttpResponseRedirect,Http404, request
from .email import send_welcome_email
from .models import Comment, Profile, Projects, Rating
from .forms import NewSiteForm, RatingForm, UpdateProfile
import datetime as dt
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectsSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from django.http import JsonResponse


# Custom 404 page
def handle_not_found(request, exception):
    
    return render(request, 'errors/404.html')

# Create your views here.
def homepage(request):
  date=dt.date.today()
  username = request.user.username
  profile = Profile.get_user(username)
  projects = Projects.objects.all().order_by('-pub_date')
  highest_rated_site = Rating.objects.order_by().annotate(avg_rating=(F('design')+ F('usability') +F('content'))/3).order_by('-avg_rating')[0]
  
  return render(request, 'main/home.html', {"date":date, "projects":projects, "highest_rated_site":highest_rated_site, "profile": profile})

def about(request):
    username = request.user.username
    profile = Profile.get_user(username)
  
    return render(request, 'main/about.html', {"username":username, "profile":profile})

@login_required
def welcome_mail(request):
  user=request.user
  email=user.email
  name=user.username
  send_welcome_email(name,email)
  return redirect(create_profile)

@login_required
def create_profile(request):
  current_user=request.user
  if request.method == 'POST':
    form = CreateProfileForm(request.POST,request.FILES)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = current_user
      profile.save()
    return HttpResponseRedirect('/')
  else:
    form = CreateProfileForm()
  return render(request,'profile/create_profile.html',{"form":form})

# Profile page
@login_required
def user_profile(request, username):
    '''
    Method to display a specific user profile
    '''
    profile = Profile.get_user(username)
    projects = Projects.user_projects(username)
    
    return render(request, 'profile/user_profile.html', {"profile": profile, "projects":projects })
  
@login_required
def new_site(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewSiteForm(request.POST, request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = current_user
            site.save()
        return redirect('home')

    else:
        form = NewSiteForm()
    return render(request, 'project/submit_site.html', {"form": form})

@login_required  
def search(request):
    username = request.user.username
    profile = Profile.get_user(username)

    if 'search' in request.GET and request.GET["search"]:
        name = request.GET.get("search")
        searched_projects = Projects.search_project(name).order_by('-pub_date')
        print(searched_projects)
        message = f"{name}"

        return render(request, 'project/search_project.html',{"message":message,"projects": searched_projects, "username":username, "profile":profile})

    else:
        message = "You haven't searched for any term"
        
        return render(request, 'project/search_project.html',{"message":message})

@login_required
def single_site(request,project_id):
    current_user = request.user
    username = request.user.username
    profile = Profile.get_user(username)
    project = Projects.objects.get(id = project_id)
    comments = Comment.objects.filter(project__id__contains = project_id).order_by('-pub_date')
    ratings = Rating.objects.filter(project__id__contains=project_id).annotate(avg_rating=(F('design') + F('usability') + F('content'))/3).order_by('-avg_rating')
    logic = ratings.filter(user__username__icontains=current_user.username)
    design_list = []
    design_rating = 0
    usability_list = []
    usability_rating = 0
    content_list = []
    content_rating = 0
    
    for rating in ratings: 
        design_list.append(rating.design)
        design_rating = sum(design_list)/len(design_list)
        usability_list.append(rating.usability)
        usability_rating = sum(usability_list)/len(usability_list)
        content_list.append(rating.content)
        content_rating = sum(content_list)/len(content_list)
       
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = current_user
            rating.project = project
            rating.save()
        return redirect('single_site', project_id)

    else:
        form = RatingForm()
        context = {
            'comments':comments,
            'project':project, 
            'username':username, 
            'profile':profile, 
            'form':form,
            'ratings':ratings, 
            'design_rating' : design_rating,
            'usability_rating' : usability_rating, 
            'content_rating' : content_rating, 
            'logic':logic

            }
    
    return render(request,"project/single_site.html", context)

@login_required
def comment(request,project_id):
    '''
    Method to add post comments
    '''
    project = Projects.objects.get(pk=project_id)
    comments = request.GET.get("comments")
    current_user = request.user
    comment= Comment(project = project, comment = comments, user = current_user)
    comment.save_comment()

    return redirect('single_site', project.pk)

@login_required
def update_profile(request,username):
  user=User.objects.get(username=username)
  current_user = request.user
  
  if request.method =='POST':
    form = UpdateProfile(request.POST,request.FILES, instance=current_user.profile)
    
    if form.is_valid():
      form.save()
      return redirect('profile', user.username)
  
  else:
    form = UpdateProfile(instance=current_user.profile)
  
  return render(request,"profile/update_profile.html", {"form":form})


# /////////APIs/////////////

class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializers = ProfileSerializer(profiles, many=True)
        return Response(serializers.data)
      
    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    
class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)    
      
      
class ProjectsList(APIView):
    permission_classes = (IsAdminOrReadOnly,)  
    def get(self, request, format=None):
        projects = Projects.objects.all()
        serializers = ProjectsSerializer(projects, many=True)
        return Response(serializers.data)      
      
    def post(self, request, format=None):
        serializers = ProjectsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
    
class ProjectDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_project(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectsSerializer(project)
        return Response(serializers.data)        