from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    text = models.TextField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_answered = models.BooleanField(default=True)  # Add this field


class Answer(models.Model):
    text = models.TextField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

