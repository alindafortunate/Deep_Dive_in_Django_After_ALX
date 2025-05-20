import markdown
from django.template.defaultfilters import truncatewords
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import Post

class LatestPostFeed(Feed):
    title='My Blog'
    link=
