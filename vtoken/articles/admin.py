from django import forms
from django.contrib import admin
from django.db import models
from .models import Article, Scriblers, MultiMedia


admin.site.register(Article)
admin.site.register(Scriblers)
admin.site.register(MultiMedia)
