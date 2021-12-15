from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.homepage, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('email/',views.welcome_mail,name='email'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile/<username>',views.user_profile,name='profile'),
    path('new/site', views.new_site, name='new_site'),
    path('search/', views.search, name='search'),
    path('update_profile/<username>',views.update_profile,name='update_profile'),
    re_path(r'^site/(\d+)',views.single_site,name ='single_site'),
    re_path('comment/(?P<project_id>\d+)',views.comment,name='addComment'),

    # *************FOR API REQUESTS*****************
    path('api/profiles/', views.ProfileList.as_view()),
    path('api/projects/', views.ProjectsList.as_view()),
    re_path(r'api/profile/profile-id/(?P<pk>[0-9]+)/$', views.ProfileDescription.as_view()),
    re_path(r'api/project/project-id/(?P<pk>[0-9]+)/$', views.ProjectDescription.as_view()),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
