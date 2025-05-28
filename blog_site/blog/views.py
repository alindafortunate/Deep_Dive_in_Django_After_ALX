from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count
from django.views.decorators.http import require_POST

from taggit.models import Tag
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm


class PostListView(ListView):
    """An alternative to the post_list function based view"""

    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = "posts"

    template_name = "blog/post/list.html"


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )
    form = CommentForm()
    comments = post.comments.filter(active=True)
    # Retrieving related posts by tags.
    post_tag_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)

    # Retrieving one post incase the same posts have the same tags, and also returning 4 posts by slicing.
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    # You can even use the similar_objects() method from taggit
    #  to retrieve the similar objects that have the same tag
    # similiar_objects = post.tags.similar_objects()
    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "form": form,
            "comments": comments,
            "similar_posts": similar_posts,
        },
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']})" f" Recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url} \n\n"
                f"{cd['name']}'s comments: {cd['comment']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        "blog/post/share.html",
        {
            "post": post,
            "form": form,
            "sent": sent,
        },
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


# On 21st/May/2025 I was engaged with Building Tomorrow work, so I didn't code.
# On 23rd/May/2025 I was engaged with the donor visit (Building Tomorrow work) and I didn't code.
# On 24th/May/2025 I was engaged with the thanks giving ceremony of Madam Rhonah, and I didn't code.


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gte=0.3)
                .order_by("-rank")
            )
    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )
