from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import AskQuestionForm, AnswerQuestionForm
from .models import Question, Answer
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='user_login')
def question_list(request):
    questions = Question.objects.all()
    ask_question_form = AskQuestionForm()

    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            new_question = Question.objects.create(
                customer=request.user if request.user.is_authenticated else None,
                text=question_text
            )
            return redirect('question_list')
    else:
        form = AskQuestionForm()

    return render(request, 'question_list.html', {'questions': questions, 'ask_question_form': form})


def ask_question(request):
    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            # Create a new question and save it to the database
            question_text = form.cleaned_data['question_text']
            new_question = Question.objects.create(customer=request.user, text=question_text)
            return redirect('question_list')
    else:
        form = AskQuestionForm()

    return render(request, 'ask_question.html', {'form': form})


def answer_question(request):
    if request.method == 'POST':
        form = AnswerQuestionForm(request.POST)
        if form.is_valid():
            # Create a new answer and save it to the database
            question = form.cleaned_data['question']
            answer_text = form.cleaned_data['answer_text']
            new_answer = Answer.objects.create(customer=request.user, question=question, text=answer_text)
            return redirect('question_list')
    else:
        form = AnswerQuestionForm()

    return render(request, 'answer_question.html', {'form': form})

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if the passwords match
        if password == password2:

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                # Handle the case where the username already exists
                return render(request, "register.html", {"error_message": "Username already exists"})

            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            # Redirect to the desired page after registration (e.g., 'question_list')
            return redirect('question_list')
        else:
            # Handle the case where the passwords don't match
            return render(request, "register.html", {"error_message": "Passwords do not match"})

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            # Redirect to the desired page after login (e.g., 'question_list')
            return redirect('question_list')
        else:
            # Handle the case where authentication fails
            return render(request, "login.html", {"error_message": "Login failed. Please check your credentials."})

    return render(request, "login.html")