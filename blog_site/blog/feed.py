import markdown
from django.template.defaultfilters import truncatewords_html
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    title = "My Blog"
    link = reverse_lazy("blog:post_list")
    description = "This is the latest content."

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
