from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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

