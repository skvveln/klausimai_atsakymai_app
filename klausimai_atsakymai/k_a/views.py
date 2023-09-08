from django.shortcuts import render
from .models import Question, Answer
# Create your views here.

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})