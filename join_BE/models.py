from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Contacts(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = PhoneNumberField(blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.user.first_name})"

class Tasks(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    assigned_to = models.JSONField(default=list)
    due_date = models.DateField()
    prio = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('urgent', 'Urgent')])
    category = models.CharField(max_length=20, choices=[('Technical Task', 'Technical Task'), ('User Story', 'User Story')])
    PositionID = models.CharField(max_length=20, blank=True, null=True)

class Subtask(models.Model):
    task = models.ForeignKey(Tasks, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.BooleanField(default=False)