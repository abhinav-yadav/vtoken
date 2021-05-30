from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

import string
import random

from .models import (
    Quiz,
    Question,
    Option,
    Response,
    Record,
)

def create_quiz_slug():
        slug =''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        try:
            data = get_object_or_404(Quiz, slug=slug)
            return create_quiz_slug()
        except:
            return slug

@receiver(pre_save, sender = Quiz)
def quiz_slug(sender, instance, *args, **kwargs):
    if instance.title:
        slug = create_quiz_slug()
        instance.slug = slug
