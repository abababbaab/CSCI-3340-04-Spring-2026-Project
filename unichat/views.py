from concurrent.futures import thread
from mailbox import Message

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Thread, Messagess, Assignments, Quiz, Test, AssignMessage, QMessage, TMessage, ChatMessage
from .forms import UserUpdateForm, ProfileUpdateForm, ThreadForm, MessageForm, AssignForm, AssignMessForm, QuizForm, \
    QuizMessForm, TMessForm, TestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Course
from .forms import CourseForm
# Create your views here.
def home(request):
    return render(request,'home.html',{})

@login_required
def chat(request):
    courses = Course.objects.all().order_by('name')
    return render(request, 'chat.html', {'courses': courses})
@login_required
def classdash(request):
    return render(request,'clsdash.html',{})
@login_required
def classedit(request):
    return render(request,'clsedit.html',{})
@login_required
def classcode(request):
    return render(request,'clscode.html',{})
@login_required
def postedit(request):
    return render(request,'postedit.html',{})


#thread stuff
#------------------------
@login_required
def thrd_list(request):
    threads = Thread.objects.order_by('-created_at')
    return render(request, 'studquest.html', {'threads': threads})
@login_required
def thrd_detail(request,pk):#thrd_id
    #thread = Thread.objects.get(id=thrd_id)#<--= get_object_or_404(Thread, pk=pk)
    #Posts = Post.objects.filter(thread=thread).order_by('-created_on')
    thread = get_object_or_404(Thread, pk=pk)
    messagess = thread.messagess.order_by('created_at')
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.thread = thread
            msg.author = request.user
            msg.save()
            return redirect('threaddetail',pk=pk)#<- thrd_id
    else:
        form = MessageForm()
    return render(request,'thrddetail.html',{
                        "form":form, 'thread':thread,'messagess':messagess})
@login_required
def thrd_create(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()
            return redirect('threaddetail', pk=thread.pk)
    else:
        form = ThreadForm()
    return render(request,'thrdcreate.html',{"form":form})
@login_required
def edit_thread(request,pk):
    thread = get_object_or_404(Thread, pk=pk)
    if thread.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('threaddetail',pk=thread.pk)#pk
    else:
        form = ThreadForm(instance=thread)
    return render(request, 'edit_thread.html', {'form': form, 'thread': thread})
@login_required
def edit_message(request,pk):
    message = get_object_or_404(Messagess, pk=pk)
    if message.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('threaddetail',pk=message.thread.pk)
    else:
        form = MessageForm(instance=message)
    return render(request, 'edit_mess.html', {'form': form, 'message': message})
@login_required
def delete_thread(request,pk):
    thread = get_object_or_404(Thread, pk=pk)
    if thread.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        thread.delete()
        return redirect('studentquestions')
    return render(request, 'del_thread.html', {'thread': thread})
@login_required
def delete_message(request,pk):
    message = get_object_or_404(Messagess, pk=pk)
    if message.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        thread_pk = message.thread.pk
        message.delete()
        return redirect('threaddetail',pk=thread_pk)
    return render(request, 'del_mess.html', {'message': message})
#assigments
#------------------------------------------------------------------------------------------------
@login_required
def assign_detail(request,pk):
    assignment = get_object_or_404(Assignments, pk=pk)
    messagess = assignment.messagess.order_by('-created_at')
    if request.method == "POST":
        form = AssignMessForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.assignment = assignment
            msg.author = request.user
            msg.save()
            return redirect('assignmentdetail',pk=assignment.pk)
    else:
        form = AssignMessForm()
    return render(request, 'assignm_det.html', {'assignment': assignment,
                                                'form': form, 'messagess': messagess})
@login_required
def assign_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = AssignForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.created_by = request.user
            assignment.save()
            return redirect('assignmentdetail',pk=assignment.pk)
    else:
        form = AssignForm()
    return render(request, 'assign_create.html', {'form': form})
@login_required
def edit_assignment(request,pk):
    assignment = get_object_or_404(Assignments, pk=pk)
    if assignment.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = AssignForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignmentdetail',pk=assignment.pk)
    else:
        form = AssignForm(instance=assignment)
    return render(request, 'edit_assignment.html', {'form': form,
                                                    'assignment': assignment})

@login_required
def del_assignment(request,pk):
    assign = get_object_or_404(Assignments, pk=pk)
    if assign.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        course_pk = assign.course.pk
        assign.delete()
        return redirect('course_detail', pk=course_pk)
    return render(request, 'del_assign.html', {'assign': assign})
@login_required
def edit_amessage(request,pk):
    amessage = get_object_or_404(AssignMessage, pk=pk)
    if amessage.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = AssignMessForm(request.POST, instance=amessage)
        if form.is_valid():
            form.save()
            return redirect('assignmentdetail',pk=amessage.assignment.pk)
    else:
        form = AssignMessForm(instance=amessage)
    return render(request, 'edit_amess.html', {'form': form, 'message': amessage})
@login_required
def del_amessage(request,pk):
    amessage = get_object_or_404(AssignMessage, pk=pk)
    if amessage.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        assignment_pk = amessage.assignment.pk
        amessage.delete()
        return redirect('assignmentdetail',pk=assignment_pk)
    return render(request, 'del_amess.html', {'amessage': amessage})
#quiz
#-------------------------------------------------------------------
@login_required
def quiz_detail(request,pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    messagess = quiz.messagess.order_by('-created_at')
    if request.method == "POST":
        form = QuizMessForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.quiz = quiz
            msg.author = request.user
            msg.save()
            return redirect('quizdetail',pk=quiz.pk)
    else:
        form = QuizMessForm()
    return render(request, 'quiz_det.html', {'quiz': quiz,
                                             'form': form, 'messagess': messagess})
@login_required
def quiz_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.created_by = request.user
            quiz.save()
            return redirect('quizdetail',pk=quiz.pk)
    else:
        form = QuizForm()
    return render(request, 'quiz_create.html', {'form': form})
@login_required
def edit_quiz(request,pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if quiz.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quizdetail',pk=quiz.pk)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'edit_quiz.html', {'form': form, 'quiz': quiz})
@login_required
def del_quiz(request,pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if quiz.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        course_pk = quiz.course.pk
        quiz.delete()
        return redirect('course_detail',pk=course_pk)
    return render(request, 'del_quiz.html', {'quiz': quiz})
@login_required
def edit_qmessage(request,pk):
    message = get_object_or_404(QMessage, pk=pk)
    if message.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = QuizMessForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('quizdetail',pk=message.quiz.pk)
    else:
        form = QuizMessForm(instance=message)
    return render(request, 'edit_qmess.html', {'form': form, 'message': message})
@login_required
def del_qmessage(request,pk):
    qmessage = get_object_or_404(QMessage, pk=pk)
    if qmessage.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        quiz_pk = qmessage.quiz.pk
        qmessage.delete()
        return redirect('quizdetail',pk=quiz_pk)
    return render(request, 'del_qmess.html', {'qmessage': qmessage})

#test
#---------------------------------------------------------
@login_required
def test_detail(request,pk):
    test = get_object_or_404(Test, pk=pk)
    messagess = test.messagess.order_by('-created_at')
    if request.method == "POST":
        form = TMessForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.test = test
            msg.author = request.user
            msg.save()
            return redirect('testdetail',pk=test.pk)
    else:
        form = TMessForm()
    return render(request, 'test_det.html', {'test': test,
                                             'form': form, 'messagess': messagess})
@login_required
def test_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.course = course
            test.created_by = request.user
            test.save()
            return redirect('testdetail',pk=test.pk)
    else:
        form = TestForm()
    return render(request, 'test_create.html', {'form': form})
@login_required
def edit_test(request,pk):
    test = get_object_or_404(Test, pk=pk)
    if test.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('testdetail',pk=test.pk)
    else:
        form = TestForm(instance=test)
    return render(request, 'edit_test.html', {'form': form, 'test': test})
@login_required
def del_test(request,pk):
    test = get_object_or_404(Test, pk=pk)
    if test.created_by != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        course_pk = test.course.pk
        test.delete()
        return redirect('course_detail',pk=course_pk)
    return render(request, 'del_test.html', {'test': test})
@login_required
def edit_tmessage(request,pk):
    message = get_object_or_404(TMessage, pk=pk)
    if message.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = TMessForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('testdetail',pk=message.test.pk)
    else:
        form = TMessForm(instance=message)
    return render(request, 'edit_tmess.html', {'form': form, 'message': message})
@login_required
def del_tmessage(request,pk):
    tmessage = get_object_or_404(TMessage, pk=pk)
    if tmessage.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        test_pk = tmessage.test.pk
        tmessage.delete()
        return redirect('testdetail',pk=test_pk)
    return render(request, 'del_tmess.html', {'tmessage': tmessage})



#login/register system
#-----------------------------------
def register(request):      #okok so just use django form
    if request.method == "POST":    #need POST
        form = UserCreationForm(request.POST)   #<---form from django
        if form.is_valid(): #check if valid
            form.save()
            messages.success(request, "Account created successfully!")
            print("User created successfully")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":    #needs POST
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            print("User profile udpated successfully")
            return redirect("home")  #change later to home or dash
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    #if not POST or valid forms then retry by sending to same page
    return render(request, "profile.html", {"u_form": u_form, "p_form": p_form})


#--------------------------------------------------------------------------------------------------------
@login_required
def course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form, 'action': 'Create'})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, created_by=request.user)
    assignments = Assignments.objects.filter(course=course).order_by('-created_at')
    quizs = Quiz.objects.filter(course=course).order_by('-created_at')
    tests = Test.objects.filter(course=course).order_by('-created_at')
    return render(request, 'course_detail.html',
                  {'course': course,'assignments': assignments,
                   'quizs': quizs, 'tests': tests})

#chat_messaging----------------------------------------------------------------------
from django.http import JsonResponse
import json
from .models import ChatMessage

@login_required
def get_messages(request, course_id):
    messages_qs = ChatMessage.objects.filter(
        course_id=course_id
    ).order_by('created_at').values(
        'author__username', 'body', 'created_at'
    )
    data = [
        {
            'author': m['author__username'],
            'body': m['body'],
            'created_at': m['created_at'].strftime('%H:%M'),
            'is_me': m['author__username'] == request.user.username
        }
        for m in messages_qs
    ]
    return JsonResponse(data, safe=False)

@login_required
def send_message(request, course_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        body = data.get('body', '').strip()
        if body:
            course = get_object_or_404(Course, pk=course_id)
            ChatMessage.objects.create(
                course=course,
                author=request.user,
                body=body
            )
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

