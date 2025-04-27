from django.shortcuts import render
from .models import Post


def list_posts(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "index.html", context)


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    context = {"post": post}
    return render(request, "detail.html", context)
