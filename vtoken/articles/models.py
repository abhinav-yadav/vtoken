from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

from django_comments_xtd.moderation import moderator, XtdCommentModerator
from taggit.managers import TaggableManager

from markdown_deux import markdown
from ckeditor.fields import RichTextField

from .utils import get_read_time



def upload_location(instance, filename):
    ArticleModel = instance.__class__
    try:
        new_id = ArticleModel.objects.order_by("id").last().id + 1
    except Exception as e:
        new_id = 1

    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)


class Article(models.Model):
    author = models.ForeignKey(User , default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique = True)
    image = models.ImageField(upload_to = upload_location,
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field",
            default='default.jpg')
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    digest = RichTextField(config_name='digest',null = True, max_length=500)
    content = RichTextField()
    publish = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    allow_comments = models.BooleanField('allow comments', default=True)
    tags = TaggableManager()
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("articles:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("articles:like-api-toggle", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def snippet(self):
        return self.body[:50]+ '...'

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def create_slug(instance):
    slug = slugify(instance.title)
    qs = Article.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        qs = Article.objects.order_by("-id")
        slug = "%s-%s" %(slug, qs.first().id)
    return slug


def pre_save_article_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_article_receiver, sender=Article)


class ArticleCommentModerator(XtdCommentModerator):
    removal_suggestion_notification = True

moderator.register(Article, ArticleCommentModerator)



class Scriblers(models.Model):
    article_id = models.ForeignKey( Article, default=None, on_delete=models.CASCADE)
    scribler = models.CharField(max_length = 100 , blank =True)

    def __str__(self):
        return self.scribler

def file_upload(instance, filename):
    file_path = '{article_id}/files/{tree}/{filename}'.format(
         article_id = instance.article_id.id, tree = instance.tree,filename = filename)
    return file_path

class MultiMedia(models.Model):
    article_id = models.ForeignKey(Article , default=None, on_delete=models.CASCADE)
    tree  = models.CharField(max_length = 500, default = None, null=True, blank =True)
    file = models.FileField(upload_to = file_upload , blank =True, max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length = 100 , default = None )

    def __str__(self):
        s =str(self.file)
        return s
