from threading import Thread

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
#off for login thread
#@receiver(post_save, sender = User)
#def create_thread(sender, instance, created, **kwargs):
#	if created:
#		Thread.objects.create(user=instance)