from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('chat/', views.chat, name='chat'),

    #path('', views.home, name ='home'),
    #path('chat/', views.chat, name ='chat'),
    path('dash/', views.classdash, name ='dashboard'),
    path('classedit/', views.classedit, name ='classedit'),
    path('classcode/', views.classcode, name ='classcode'),
    path('postedit/', views.postedit, name ='postedit'),
#treadstuff
    #----------------------------------------------------
    path('studentquestions/', views.thrd_list, name ='studentquestions' ),
    path('<int:pk>/', views.thrd_detail, name ='threaddetail'),#<-<int:thrd_id
    path('newquestion/', views.thrd_create, name ='threadcreate'),
#login/profile stuff
#---------------------------------------
#login does not use a view
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name ='register'),
    path('accounts/profile/', views.profile, name ='profile'),
#-----------------------------
#course stuff
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
#---------------------------------------------------------------------------------
#assignment stuff
    path('assignmentcreate/<int:pk>', views.assign_create, name='assignment_create'),
    path('assignments/<int:pk>/', views.assign_detail, name='assignmentdetail'),


]