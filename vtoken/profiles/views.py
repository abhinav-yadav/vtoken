from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile , Profileimage
from . forms import UserForm , ProfileForm, DpForm


from core.models import Quiz


decorators = [login_required(login_url = "/accounts/login/")]
decorators_1 = [transaction.atomic] + decorators



@method_decorator(decorators , name='dispatch')
class ProfileArticles(View):

    def get(self, request, slug):
        instance = User.objects.get(username=slug)
        id = instance.id
        profile = Profile.objects.get(user=id)
        articles = instance.article_set.all()
        instance = request.user
        data = {'profile':profile , 'user':instance , 'articles' : articles}
        return render(request,'profiles/profile_articles.html',data)

method_decorator(decorators , name='dispatch')
class ProfileQuizes(View):

    def get(self, request, slug):
        instance = User.objects.get(username=slug)
        id = instance.id
        profile = Profile.objects.get(user=id)
        quizes = Quiz.objects.filter(author = instance)
        instance = request.user
        data = {'profile':profile , 'user':instance , 'quizes' : quizes}
        return render(request,'profiles/profile_quizes.html',data)


@method_decorator(decorators_1 , name='dispatch')
class ProfileUpdate(View):

    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        context={
        'user_form': user_form,
        'profile_form': profile_form,
        }

        return render(self.request, 'profiles/profile_update.html', context )

    def post(self,request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile )

        if user_form.is_valid() and profile_form.is_valid():
            instance = user_form.save(commit=False)
            instance = instance.username
            user_form.save()

            profile_instance = profile_form.save(commit=False)
            profile_instance.save()

            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profiles:profile',slug = instance )
        else:
            context={
            'user_form': user_form,
            'profile_form': profile_form,
            }
            messages.error(request, ('Please correct the error below.'))
            return render(self.request, 'profiles/profile_update.html', context )

class DpUpdate(View):
    def get(self, request):
        form = DpForm(instance = request.user)

        context = {
        'form' : form,
        }
        return render(self.request, 'profiles/dp_update.html', context)

    def post(self, request):
        form = DpForm(request.POST,request.FILES ,instance=request.user.profileimage)
        if form.is_valid():
            form.save()
            return redirect('profiles:dp_update')
        else:
            messages.error(request, ('Update was unsuccessful'))
            context = {
            'form' : form,
            }
            return render(self.request, 'profiles/dp_update.html', context)
