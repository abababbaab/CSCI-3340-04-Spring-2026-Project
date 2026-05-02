from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Thread, Messagess, Course, Assignments, Quiz, Test
from .forms import UserUpdateForm, ProfileUpdateForm, ThreadForm, MessageForm, CourseForm, AssignmentForm, QuizForm, TestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request,'home.html',{})

def chat(request):
    return render(request, "chat.html", {})

def classdash(request):
    return render(request,'clsdash.html',{})
def classedit(request):
    return render(request,'clsedit.html',{})
def classcode(request):
    return render(request,'clscode.html',{})
def postedit(request):
    return render(request,'postedit.html',{})


def thrd_list(request):
    threads = Thread.objects.order_by('-created_at')
    return render(request, 'studquest.html', {'threads': threads})

def thrd_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    messagess = thread.messagess.order_by('created_at')
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.thread = thread
            msg.author = request.user
            msg.save()
            return redirect('threaddetail', pk=pk)
    else:
        form = MessageForm()
    return render(request,'thrddetail.html',{"form":form, 'thread':thread,'messagess':messagess})

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

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "profile.html", {"u_form": u_form, "p_form": p_form})


def course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'course_list.html', {'courses': courses})

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

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    assignments = Assignments.objects.filter(course=course)
    quizs = Quiz.objects.filter(course=course)
    tests = Test.objects.filter(course=course)
    return render(request, 'course_detail.html', {
        'course': course,
        'assignments': assignments,
        'quizs': quizs,
        'tests': tests,
    })

#assignment stuff
#----------------------------
def assign_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.created_by = request.user
            assignment.save()
            return redirect('course_detail', pk=pk)
    else:
        form = AssignmentForm()
    return render(request, 'assign_create.html', {'form': form, 'course': course})

def assign_detail(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk)
    return render(request, 'assignm_det.html', {'assignment': assignment})


def quiz_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.created_by = request.user
            quiz.save()
            return redirect('course_detail', pk=pk)
    else:
        form = QuizForm()
    return render(request, 'assign_create.html', {'form': form, 'course': course})

def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'assignm_det.html', {'assignment': quiz})


def test_create(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.course = course
            test.created_by = request.user
            test.save()
            return redirect('course_detail', pk=pk)
    else:
        form = TestForm()
    return render(request, 'assign_create.html', {'form': form, 'course': course})

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'assignm_det.html', {'assignment': test})