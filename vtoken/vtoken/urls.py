from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import (
     Home,
     about,
     Setting,
     Activity,
     Completed,
     Created,
     ArticleList,
     autoCompleteView,
     searchAutoComplete,
     Search,
     StudentLoginView,
     UserType,
     ActiveAssignment,
     ActiveQuiz,

)
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('profile/',include('profiles.urls')),
    path('articles/',include('articles.urls')),
    path('admin/', admin.site.urls),
    path('quiz/', include("core.urls")),
    path('about/', about , name = 'about'),
    path('settings/', Setting.as_view(), name='setting'),
    path('activity/', Activity.as_view(), name= 'activity'),
    path('completed/', Completed.as_view(), name= 'completed'),
    path('created/', Created.as_view(), name = 'created'),

    # instructor specifi urls
    path('active/quiz/', ActiveQuiz.as_view(), name= 'instructor-active-quiz'),
    path('active/assgnments/',ActiveAssignment.as_view(), name= 'instructor-active-assignment'),


    path('login/', UserType.as_view(), name ='usertypelogin'),
    path('accounts/login/student/', StudentLoginView.as_view(), name='student-login'),

    path('articlelist/', ArticleList.as_view(), name='article_editlist'),
    path('search/', Search.as_view(), name='search'),
    path('autocomplete/', autoCompleteView, name='autocomplete'),
    path('search-autocomplete/', searchAutoComplete, name='search-autocomplete'),
    path('', Home.as_view(), name='home'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('comments/', include('django_comments_xtd.urls')),
    path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('autocomplete/', autoCompleteView, name='autocomplete'),
    path('search-autocomplete/', searchAutoComplete, name='search-autocomplete'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
