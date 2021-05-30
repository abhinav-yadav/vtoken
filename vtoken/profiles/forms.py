from PIL import Image
from django.core.files import File
from django import forms
from . import models
from django.contrib.auth.models import User
from . models import Profile , Profileimage, Academicdetails

# class AcademicdetailsForm(forms.ModelForm):
#     class Meta:
#         model = Academicdetails
#         fields  = ('college', 'college_id', 'course')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('role' ,'gender','website','bio' ,'dob','linkedin' ,'twitter' ,'github',)


class DpForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profileimage
        fields = ('profile_image', 'x', 'y', 'width', 'height',)

    def save(self):
        photo = super(DpForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.profile_image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.profile_image.path)

        return photo
