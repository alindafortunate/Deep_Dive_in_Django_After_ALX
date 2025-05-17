from django import template
from ..models import Post

register = template.Library()


def total_posts():
    return Post.published.count()
