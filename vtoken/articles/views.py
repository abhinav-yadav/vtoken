import mimetypes
import os
from django.conf import settings


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages

from hitcount.views import HitCountDetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import Article, Scriblers, MultiMedia
from . import forms
from profiles.models import Profile

from taggit.models import Tag

def get_file_tree(dire):
    dire = dire[1:-1]
    dire = list(dire.split(','))
    d={}
    for i in dire:
        temp =  list(i.split(':'))
        temp[0] = temp[0][1:-1]
        temp[1] = temp[1][1:-1]
        temp[1] = temp[1][:temp[1].rfind('/')]
        d[temp[0]] = temp[1]
    return(d)

def get_mime_type(file):
    type = mimetypes.guess_type(file)
    return type


decorators = [login_required(login_url = "/accounts/login/")]
decorators_1 = [transaction.atomic] + decorators
multimedia_context = {
    'image' : ['jpg' , 'gif','png']

}


#-----> article form , scribler form , file form
@method_decorator(decorators, name='dispatch')
class ArticleCreate(View):

    def get(self, request):
        articleform = forms.CreateArticleForm(request.GET or None)
        # formset = forms.AuthorFormset(queryset=Scriblers.objects.none())
        context = {
            'articleform': articleform,
            # 'formset': formset,
                }
        return render(self.request , 'articles/article_create.html',context)


    def post(self, request):

        articleform = forms.CreateArticleForm(request.POST or None)
        # formset = forms.AuthorFormset(request.POST)

        if articleform.is_valid():

            article = articleform.save(commit=False)
            article.author = request.user
            if 'image' in request.FILES:
                article.image = request.FILES['image']
            article.content = article.digest
            article.save()
            articleform.save_m2m()

            # for form in formset:
            #     author = form.save(commit=False)
            #     if author.scribler:
            #         author.article_id = article
            #         author.save()

            messages.success(request, ('Your article "{} !" as been Created'.format(article.title)))
            return redirect('articles:article_content' , pk = article.id)
        else :
            messages.error(request, ('Please correct the error below.'))
            context = {
                'articleform': articleform,
                    }
            return render(self.request , 'articles/article_create.html',context)


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Article, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_



class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Article, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)


@method_decorator(decorators, name='dispatch')
class ScriblerAdd(View):

    def get(self, request,slug):
        article = get_object_or_404(Article , slug = slug )
        scriblers =Scriblers.objects.filter(article_id=article.id)
        author = []
        anonymous_authors=[]
        for scribler in scriblers:
            try:
                author.append(get_object_or_404(User , username = scribler ))
            except:
                anonymous_authors.append(scribler)
        form = forms.ScriblerForm()
        context = {
            'form': form,
            'article': article,
            'authors' : author,
            'anonymous_authors':anonymous_authors
                }
        return render(self.request , 'articles/scribler_edit.html',context)


    def post(self, request,slug):
        article = get_object_or_404(Article , slug = slug )
        form = forms.ScriblerForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            if author.scribler:
                try:
                    exists = get_object_or_404(Scriblers , scribler = author.scribler,article_id=article.id )
                    messages.error(request, ('author is present'))
                except:
                    author.article_id = article
                    author.save()
                    messages.success(request, ('Your authors of  "{} !" as been updated'.format(article.title)))
            return redirect('articles:edit_scribler', slug=article.slug)
        else :
            messages.error(request, ('Please correct the error below.'))
            scriblers =Scriblers.objects.filter(article_id=article.id)
            author = []
            anonymous_authors=[]
            for scribler in scriblers:
                try:
                    author.append(get_object_or_404(User , username = scribler ))
                except:
                    anonymous_authors.append(scribler)
            context = {
                'form': form,
                'article': article,
                'authors' : author,
                'anonymous_authors':anonymous_authors
                    }
            return render(self.request , 'articles/scribler_edit.html',context)


@method_decorator(decorators_1 , name='dispatch')
class ScriblerDelete(View):
    def get(self, request, pk):
        article = get_object_or_404(Article , id = pk )
        scriblers = Scriblers.objects.filter(article_id=article.id)
        author = []
        anonymous_authors=[]
        for scribler in scriblers:
            try:
                author.append(get_object_or_404(User , username = scribler ))
            except:
                anonymous_authors.append(scribler)
        context={
         'article': article,
         'authors' : author,
         'anonymous_authors':anonymous_authors
        }
        return render(request,'articles/scribler_delete.html' , context)

    def post(self,request,pk):
        article = get_object_or_404(Article , id = pk )
        author = request.POST.get('q')
        scribler = get_object_or_404(Scriblers, article_id=article.id ,scribler=author )
        scribler.delete()
        return redirect('articles:delete_scribler',pk=pk)



@method_decorator(decorators, name='dispatch')
class ArticleFilesEdit(View):

    def get(self, request, slug):
        article = get_object_or_404(Article , slug = slug )
        files = MultiMedia.objects.filter(article_id=article.id)
        form = forms.MultiMediaForm(request.GET or None)
        context = {
            'article' : article,
            'form' :form, 'files' : files,
            'image' : ['png','jpg','gif'],
        }
        return render(self.request, 'articles/attachments.html' ,context )

    def post(self, request, slug):
        article = get_object_or_404(Article , slug = slug )
        form = forms.MultiMediaForm(request.POST)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for f in files:
                extension = f.name.split('.')[1]
                data = MultiMedia(file=f , article_id=article , file_type=extension )
                data.save()

            messages.success(request, ('Your article "{} !" as been uploaded'.format(article.title)))
            return redirect('home')
        else :
            messages.error(request, ('Please correct the error below.'))


@method_decorator(decorators_1 , name='dispatch')
class FileDelete(View):

    def post(self,request,pk):
        file = get_object_or_404(MultiMedia , pk = pk )
        article = get_object_or_404(Article , id = file.article_id.id )
        file.delete()
        return redirect('articles:edit_attachment' , slug = article.slug )



# class ArticleDetail(View):
#
#     def get(self, request, slug):
#         article = Article.objects.get(slug=slug)
#         scriblers = Scriblers.objects.filter(article_id = article.id)
#         authors = []
#         anonymous_authors = []
#         print(scriblers)
#         for scribler in scriblers:
#             try:
#                 auth = get_object_or_404(User, username=scribler.scribler)
#                 authors.append(auth)
#             except:
#                 anonymous_authors.append(scribler.scribler)
#         context = {
#         'article':article,
#         'scriblers' : scriblers,
#         'authors' : authors,
#         'anonymous_authors' : anonymous_authors,
#          }
#
#         return render(request,'articles/article_detail.html',context)


class ArticleDetail(HitCountDetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        scriblers = Scriblers.objects.filter(article_id = context['article'])
        authors = []
        anonymous_authors = []
        for scribler in scriblers:
            try:
                auth = get_object_or_404(User, username=scribler.scribler)
                authors.append(auth)
            except:
                anonymous_authors.append(scribler.scribler)
        context.update({
        'authors' : authors,
        'anonymous_authors' : anonymous_authors,
        })
        return context

@method_decorator(decorators_1 , name='dispatch')
class ArticleDelete(View):

    def get(self,request,slug):
        article = get_object_or_404(Article , slug = slug )
        return render(self.request, 'articles/article_delete.html' , {'article':article})

    def post(self,request,slug):
        article = get_object_or_404(Article , slug = slug )
        instance = request.user
        name = article.author
        if instance == name:
            article.delete()
            messages.success(request, ('Your article "{} !" as been deleted'.format(article.title)))
            return redirect('profiles:profile' ,slug = instance)
        else:
            messages.error(request, ('your not authorized to delete !'))
            return redirect('home')



@login_required(login_url = "/accounts/login/")
@transaction.atomic
def ArticleUpdate(request, slug):
    article = get_object_or_404(Article ,slug=slug)
    if request.POST :
        if article.author == request.user :
            form = forms.CreateArticleForm(request.POST or None,request.FILES, instance=article)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                form.save_m2m()
                messages.success(request, ('Your article  as been updated'))
                article = obj
                return redirect('profiles:profile' ,slug = request.user)
            else:
                messages.error(request, ('Please correct the error below.'))
    else:
        form = forms.CreateArticleForm(instance=article)
    context ={
        'form':form ,
        'article':article,

            }
    return render(request , 'articles/article_update.html' , context)

# dont mess the below code

def tree(article,slug,request):
    directory = request.path
    index = directory.find('articles')
    directory = directory[index+len('articles'):]
    address = 'media'+'/'+directory
    address = address.replace(':','/')
    index = address.find('files')
    path = address[index:]
    path = path.replace('/',':')
    return address,path

def files_breadcrum(path):
    d={}
    path = list(path.split(':'))
    d['files'] = 'files'
    for i in range(1,len(path)):
        key=list(d)[-1]
        d[path[i]] = d[key]+':'+path[i]
    key=list(d)[-1]
    d[key]=':'
    return d


class ArticleFiles(View):

    def get(self,request,pk,slug):
        article = get_object_or_404(Article , pk = pk )
        address,path = tree(article,slug,request)
        data = os.listdir(address)
        files = []
        directories = []
        for i in data:
            check = address+'/'+i
            if os.path.isfile(check):
                files.append(i)
            else:
                directories.append(i)
        breadcrum = files_breadcrum(path)
        context = {
            'article':article,
            'directories' : directories,
            'files' :files,
            'path' : path,
            'breadcrums' : breadcrum,
            }
        return render(self.request, 'articles/article_files.html' , context )


def file_address(address):
    index = address.find('blob')
    address = address[index+len('blob/'):]
    address = address.replace(':','/')
    return address

class BlobView(View):
    def get(self,request, pk, slug):
        name = file_address(request.path)
        # the below code is for bread crum
        index = name.find('files')
        path = name[index:]
        path = path.replace('/',':')
        breadcrum = files_breadcrum(path)
        file = get_object_or_404(MultiMedia , file=name)
        type = file.file_type
        context={
            'file':file,
            'breadcrums': breadcrum,
            'article':file.article_id,
            'type' : type
        }
        print(type)
        return render(self.request, 'articles/blob.html' , context )


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    articles = Article.objects.filter(tags=tag)
    common_tags = Article.tags.most_common()[:4]
    context = {
        'tag':tag,
        'articles':articles,
        'common_tags':common_tags,
    }
    return render(request, 'homepage.html', context)

# settings

class ArticleSetting(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if request.user == article.author:
            context = {
                'article' : article,
            }
            return render(request, 'articles/article_setting.html',context)
        else:
            messages.error(request, ('you are not authorized'))
            return redirect('home')


def articleContentCreate(request, pk):
    article = get_object_or_404(Article , pk = pk)
    if request.POST:
        form = forms.ArticleContentForm(request.POST or None, instance=article)
        if form.is_valid():
            obj = form.save(commit=False)
            article.content = obj.content
            article.save()
            messages.success(request, ('Your article content is updated'))
            return redirect('profiles:profile' ,slug = request.user)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = forms.ArticleContentForm(instance=article)
    context ={
    'form':form ,
    'article': article,
    }
    return render(request , 'articles/article_content.html' , context)

def articleContentUpdate(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.author:
        if request.POST:
            form = forms.ArticleContentForm(request.POST or None, instance=article)
            if form.is_valid():
                obj = form.save(commit=False)
                article.content = obj.content
                article.save()
                messages.success(request, ('Your article content is updated'))
                return redirect('profiles:profile' ,slug = request.user)
            else:
                messages.error(request, ('Please correct the error below.'))
        else:
            form = forms.ArticleContentForm(instance=article)
        context ={
        'form':form ,
        'article': article,
        }
        return render(request , 'articles/article_content_update.html' , context)
    else:
        messages.error(request, ('you are not authorized'))
        return redirect('home')



def fileUpload(request, pk):
    article  = get_object_or_404(Article, pk=pk)
    if request.user == article.author:
        if request.POST:
            form = forms.MultiMediaForm(request.POST)
            if form.is_valid():
                directories = request.POST['directories']
                if directories:
                    tree = get_file_tree(directories)
                    files = request.FILES.getlist('file')
                    for f in files:
                        extension = get_mime_type(f.name)
                        data = MultiMedia(tree = tree[f.name] ,file=f , article_id=article, file_type=extension)
                        data.save()
                    messages.success(request, ('files as been uploaded'))
                    context={'article':article}
                    return render(request, 'articles/article_setting.html',context)
                else:
                    messages.error(request, ('form is empty'))
            else:
                messages.error(request, ('files could not be uploaded'))
        else:
            form = forms.MultiMediaForm()
        context = {
            'form':form,
            'article':article,
        }
        return render(request, 'articles/file_upload.html', context)
    else:
        messages.error(request, ('you are not authorized'))
        return redirect('home')
