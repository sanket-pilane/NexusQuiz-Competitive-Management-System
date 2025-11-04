from django import forms
from .models import Quiz, Question, Option

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'duration']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class QuestionAndOptionsForm(forms.Form):
    question_text = forms.CharField(widget=forms.Textarea)
    option1 = forms.CharField(label="Option 1")
    option2 = forms.CharField(label="Option 2")
    option3 = forms.CharField(label="Option 3")
    option4 = forms.CharField(label="Option 4")
    correct_answer = forms.ChoiceField(choices=[
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4')
    ], widget=forms.RadioSelect)
