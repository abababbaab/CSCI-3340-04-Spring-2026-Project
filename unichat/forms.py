from threading import Thread

from django import forms
from django.contrib.auth.models	import User
from .models import Profile, Thread, Messagess, Assignments, AssignMessage
from .models import Course

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields =['first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):	#extra fields
	class Meta:
		model = Profile
		fields = ['bio','age']	#phone
#thread---------------------------------------------------------------------
class ThreadForm(forms.ModelForm):
	class Meta:
		model = Thread
		fields = ['title']
class MessageForm(forms.ModelForm):
	class Meta:
		model = Messagess
		fields = ['body']
#assignment-----------------------------------------------------------------------
class AssignForm(forms.ModelForm):
    class Meta:
        model = Assignments
        fields = ['title']

class AssignMessForm(forms.ModelForm):
    class Meta:
        model = AssignMessage
        fields = ['body']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'max_students', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CSCI 3340 - Section 04'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What is this course about?'
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
        }
        labels = {
            'max_students': 'Max Students',
            'start_time': 'Chat Opens At',
            'end_time': 'Chat Closes At',
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data


