from django import forms
from .models import Question, Answer


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        required=True,
        label='Question'
    )

class AnswerQuestionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'text']  # Make sure 'text' matches the field name in the Answer model
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        required=True,
        label='Answer'
    )
