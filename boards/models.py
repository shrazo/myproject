from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Board(models.Model):
    name = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

