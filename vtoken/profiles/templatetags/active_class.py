from django.template import Library
from django.urls import reverse
register = Library()

@register.simple_tag
def is_active(request, url):
    # Main idea is to check if the url and the current path is a match
    if request.path in reverse(url):
        return "active"
    return ""

# @register.simple_tag
# def is_active_profile(request, url, slug):
#     # Main idea is to check if the url and the current path is a match
#     if request.path == reverse(url, kwargs={'slug': slug}):
#         return "active"
#     return ""

# <!-- <div class="{% is_active_profile request 'profiles:profile_article' slug=user.username %} "  >
#
# </div> -->

@register.simple_tag
def is_article_active(request, url):
    # Main idea is to check if the url and the current path is a match
    if url in request.path:
        return "active"
    return ""

@register.simple_tag
def get_query(request):
    k=request.GET
    if len(k)>0:
        return str(k['q'])
    return ""
