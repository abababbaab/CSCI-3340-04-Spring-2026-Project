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
    path('<int:pk>/edit/', views.edit_thread, name ='threadedit'),
    path('message/<int:pk>/edit', views.edit_message, name ='messedit'),
    path('<int:pk>/delete', views.delete_thread, name ='threaddelete'),
    path('message/<int:pk>/delete', views.delete_message, name ='messdelete'),
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
    path('assignments/<int:pk>/edit/', views.edit_assignment, name='assignmentedit'),
    path('amessage/<int:pk>/edit', views.edit_amessage, name='amessedit'),
    path('assignment/<int:pk>/delete', views.del_assignment, name='assignmentdelete'),
    path('amessage/<int:pk>/delete', views.del_amessage, name='amessdelete'),
#-----------------------------------------------------------------------------
#quiz stuff
    path('quizcreate/<int:pk>', views.quiz_create, name='quiz_create'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quizdetail'),
    path('quiz/<int:pk>/edit/', views.edit_quiz, name='quizedit'),
    path('qmessage/<int:pk>/edit', views.edit_qmessage, name='qmessedit'),
    path('quiz/<int:pk>/delete', views.del_quiz, name='quizdelete'),
    path('qmessage/<int:pk>/delete', views.del_qmessage, name='qmessdelete'),
#---------------------------------------------------------------------------
#test stuff
    path('testcreate/<int:pk>', views.test_create, name='test_create'),
    path('test/<int:pk>', views.test_detail, name='testdetail'),
    path('test/<int:pk>/edit/', views.edit_test, name='testedit'),
    path('tmessage/<int:pk>/edit', views.edit_tmessage, name='tmessedit'),
    path('test/<int:pk>/delete', views.del_test, name='testdelete'),
    path('tmessage/<int:pk>/delete', views.del_tmessage, name='tmessdelete'),


#chat_messaging---------------------------------------------------
path('api/messages/<int:course_id>/', views.get_messages, name='get_messages'),
path('api/messages/<int:course_id>/send/', views.send_message, name='send_message'),

#logout---------------------------------------------------
path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]