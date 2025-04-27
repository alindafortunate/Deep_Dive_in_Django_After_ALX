from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def list_posts(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "index.html", context)


def post_detail(request, pk):
    try:
        post = Post.objects.get(id=pk)
        context = {"post": post}
        return render(request, "detail.html", context)
    except Post.DoesNotExist:
        return HttpResponse("Sorry this post is not available yet.")
