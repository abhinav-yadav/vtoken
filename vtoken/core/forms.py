from django import forms
from django.forms import modelformset_factory

from .models import (
    Quiz,
    Question,
    Option,
)


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title','image','deadline','department','year']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['type','question', 'time']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['answer', 'option',]


optionformset = modelformset_factory(
    Option,
    fields = ['answer' , 'option']
)
