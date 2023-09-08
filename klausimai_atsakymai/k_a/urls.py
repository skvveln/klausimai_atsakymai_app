from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
]