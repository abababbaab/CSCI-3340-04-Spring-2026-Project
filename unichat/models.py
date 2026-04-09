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