from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Thread, Messagess
from .forms import UserUpdateForm, ProfileUpdateForm, ThreadForm, MessageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'home.html',{})


def chat(request):
    return render(request, "chat.html", {})









#def home(request):
    #return render(request,'home.html',{})
#def chat(request):
 #   return render(request,'chat.html',{})
def classdash(request):
    return render(request,'clsdash.html',{})
def classedit(request):
    return render(request,'clsedit.html',{})
def classcode(request):
    return render(request,'clscode.html',{})
def postedit(request):
    return render(request,'postedit.html',{})


#thread stuff
#------------------------
def thrd_list(request):
    threads = Thread.objects.order_by('-created_at')# _on
    return render(request, 'studquest.html', {'threads': threads})
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
            #msg.created_by = request.user #<-.author = req
            msg.author = request.user
            msg.save()
            return redirect('threaddetail',pk=pk)#<- thrd_id
    else:
        form = MessageForm()
    return render(request,'thrddetail.html',{
                        "form":form, 'thread':thread,'messagess':messagess})

def thrd_create(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()#<-form.save()
            #messages.success(request, "Thread created successfully!")
            #print("Thread created successfully")
            return redirect('threaddetail',pk=thread.pk) #<--thread.id
    else:
        form = ThreadForm()
    return render(request,'thrdcreate.html',{"form":form})


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
        form = UserCreationForm()   #form not posting but then send to retry to not lose data

    return render(request, "register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":    #needs POST
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid(): #check if valid
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            print("User profile udpated successfully")
            return redirect("profile")  #change later to home or dash
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    #if not POST or valid forms then retry by sending to same page
    return render(request, "profile.html", {"u_form": u_form, "p_form": p_form})