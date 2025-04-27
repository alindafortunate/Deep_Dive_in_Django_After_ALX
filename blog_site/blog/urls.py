from django.urls import path
from .views import list_posts, post_detail


urlpatterns = [
    path("", list_posts, name="list_posts"),
    path("post/<int:pk>/", post_detail, name="post_detail"),
]
