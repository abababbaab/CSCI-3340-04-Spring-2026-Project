from threading import Thread

from django import forms
from django.contrib.auth.models	import User
from .models import Profile, Thread, Messagess

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields =['first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):	#extra fields
	class Meta:
		model = Profile
		fields = ['bio','age']	#phone

class ThreadForm(forms.ModelForm):
	class Meta:
		model = Thread
		fields = ['title']
class MessageForm(forms.ModelForm):
	class Meta:
		model = Messagess
		fields = ['body']