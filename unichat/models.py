from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)	#basic user info from import
	#extra model variables
	bio = models.TextField(blank=True)
	age = models.IntegerField(null=True, blank=True)
	#phone = models.TextField(blank = True)
	def __str__(self):
		return self.user.username

#question thread
#---------------------------------------------------------------------
class Thread(models.Model):
	title = models.CharField(max_length=200)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.title
class Messagess(models.Model):
	thread = models.ForeignKey(Thread, related_name= 'messagess', on_delete=models.CASCADE)
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)


#class stuff
#--------------------------------------------------------------------
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    max_students = models.PositiveIntegerField(default=30)

    # Time window: when the course chat is open
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Who created it (teacher)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_open(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_time <= now <= self.end_time


#assigment
#----------------------------------------------------------------------
class Assignments(models.Model):
    course = models.ForeignKey(Course, related_name= 'assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class AssignMessage(models.Model):
    assignment = models.ForeignKey(Assignments, related_name= 'messagess', on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



