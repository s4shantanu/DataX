from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    duration = models.IntegerField()
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)  

    def __str__(self):
        return self.name



class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField()


    def __str__(self):
        return self.title


#user activity -
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"