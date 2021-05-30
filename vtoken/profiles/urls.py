from django.urls import path,include
from . import views

app_name='profiles'

urlpatterns = [
    path('edit/',views.ProfileUpdate.as_view() , name='profile_update'),
    path('image-edit/',views.DpUpdate.as_view() , name='dp_update'),
    path('articles/<slug>',views.ProfileArticles.as_view() , name='profile_article'),
    path('<slug>',views.ProfileArticles.as_view() , name='profile'),
    path('quiz/<slug>',views.ProfileQuizes.as_view() , name='profile_quiz'),
]
