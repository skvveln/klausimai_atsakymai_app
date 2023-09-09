from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import AskQuestionForm, AnswerQuestionForm
from .models import Question, Answer
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def question_list(request):
    unanswered_questions = Question.objects.filter(answers__isnull=True).order_by('-pk')  # Newest first
    answered_questions = Question.objects.filter(answers__isnull=False).order_by('-pk')  # Newest first
    ask_question_form = AskQuestionForm()
    answer_question_form = AnswerQuestionForm()

    if request.method == 'POST':
        if 'ask_question' in request.POST:
            ask_question_form = AskQuestionForm(request.POST)
            if ask_question_form.is_valid():
                ask_question = ask_question_form.save(commit=False)
                ask_question.customer = request.user
                ask_question.save()
                return redirect('question_list')
        elif 'answer_question' in request.POST:
            answer_question_form = AnswerQuestionForm(request.POST)
            if answer_question_form.is_valid():
                answer = answer_question_form.save(commit=False)
                answer.customer = request.user
                question_id = request.POST.get('question')
                if question_id:
                    question = Question.objects.get(pk=question_id)
                    answer.question = question
                    question.is_answered = True
                    question.save()
                answer.save()
                return redirect('question_list')

    return render(request, 'question_list.html', {
        'unanswered_questions': unanswered_questions,
        'answered_questions': answered_questions,
        'ask_question_form': ask_question_form,
        'answer_question_form': answer_question_form,
    })


@login_required(login_url='login')
def answer_question(request):
    if request.method == 'POST':
        answer_question_form = AnswerQuestionForm(request.POST)
        if answer_question_form.is_valid():
            answer = answer_question_form.save(commit=False)
            answer.customer = request.user

            # Get the question ID from the form
            question_id = request.POST.get('question')
            if question_id:
                question = Question.objects.get(pk=question_id)
                answer.question = question  # Associate the answer with the question
                question.is_answered = True  # Mark the question as answered
                question.save()

            answer.save()

            return redirect('question_list')  # Redirect on success

    return redirect('question_list')



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if User.objects.filter(username=username).exists():
                return render(request, "register.html", {"error_message": "Username already exists"})

            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('question_list')
        else:
            return render(request, "register.html", {"error_message": "Passwords do not match"})

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('question_list')
        else:
            return render(request, "login.html", {"error_message": "Login failed. Please check your credentials."})

    return render(request, "login.html")

