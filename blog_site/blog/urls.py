from django.urls import path
from .views import post_list, post_detail, post_share, post_comment

app_name = "blog"

urlpatterns = [
    path("", post_list, name="post_list"),
    path("tag/<slug:tag_slug>/", post_list, name="post_list_with_tag"),
    # path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", post_share, name="post_share"),
    path("post/<int:post_id>/comment/", post_comment, name="post_comment"),
]
