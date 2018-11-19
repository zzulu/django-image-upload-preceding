from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

# Create your views here.
class PostList(ListView):
    model = Post


class PostCreate(CreateView):
    model = Post
    fields = ['image','content',]
    

class PostDetail(DetailView):
    model = Post
    

class PostUpdate(UpdateView):
    model = Post
    fields = ['image','content',]
    
    
class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')