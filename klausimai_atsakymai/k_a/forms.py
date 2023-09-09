from django import forms

from .models import Question


class AskQuestionForm(forms.Form):
    question_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), required=True)

class AnswerQuestionForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), empty_label="Select a question", required=True)
    answer_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), required=True)
