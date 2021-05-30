from allauth.account.forms import SignupForm
# from profiles.forms import AcademicdetailsForm
from django import forms
from profiles.models import Academicdetails

class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        COURSE = [
        ('CSE','computer science and engineering'),
        ('IT','information technology'),
        ('ECE','electrical and communications engineering'),
        ('EEE','electrical and electronic engineering'),
        ('Mech', 'mechanical engineering'),
        ]
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['college'] = forms.CharField(required=True)
        self.fields['college_id'] = forms.CharField(max_length=10,required=True)
        self.fields['course'] = forms.ChoiceField(choices = COURSE,required=True)
        self.fields['year'] = forms.IntegerField(required=True)


    def save(self, request):
        college = self.cleaned_data.pop('college')
        college_id = self.cleaned_data.pop('college_id')
        course = self.cleaned_data.pop('course')
        user = super(MyCustomSignupForm, self).save(request)
        detais = Academicdetails(user=user,college=college,college_id=college_id,course=course)
        detais.save()
        return user
