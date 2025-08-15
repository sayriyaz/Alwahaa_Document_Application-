from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

class Document(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    submitted_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed')
    ])

    def __str__(self):
        return self.title

class Service(models.Model):
    name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])
    due_date = models.DateField()

    def __str__(self):
        return self.title

# Create your models here.
