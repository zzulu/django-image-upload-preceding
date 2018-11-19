from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import Post

# Create your views here.
class PostList(ListView):
    model = Post


# class PostCreate(CreateView):
#     model = Post
#     fields = ['image','content',]
    

# class PostDetail(DetailView):
#     model = Post
    