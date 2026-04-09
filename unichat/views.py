from django.shortcuts import render, redirect
<<<<<<< HEAD

# Create your views here.
def home(request):
    return render(request,'home.html',{})
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm
# Create your views here.
def home(request):
    return render(request,'home.html',{})

def chat(request):
    return render(request, "chat.html", {})


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
    course = get_object_or_404(Course, pk=pk, created_by=request.user)
    return render(request, 'course_detail.html', {'course': course})
>>>>>>> a1efda1 ( Added course/section creation feature)
