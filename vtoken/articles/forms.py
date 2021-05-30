from django import forms
from . import models
from django.forms import modelformset_factory

# AuthorFormset = modelformset_factory(
#     models.Scriblers,
#     fields=('scribler', ),
#     extra=1,
#     widgets={'name': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter Author Name here'
#         })
#     }
# )
#
# AuthorFormsetEdit = modelformset_factory(
#     models.Scriblers,
#     fields=('scribler','id' ),
#     extra=1,
#     widgets={'name': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter Author Name here'
#         })
#     }
# )
class ScriblerForm(forms.ModelForm):
    class Meta:
        model = models.Scriblers
        fields = ['scribler',]

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title','image','digest','tags','publish']


class MultiMediaForm(forms.ModelForm):
    class Meta:
        model = models.MultiMedia
        fields = ['file']
        widgets = {
        'file' : forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True})
        }

class ArticleContentForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['content']
