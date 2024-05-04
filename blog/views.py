from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Post


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Пост успешно создан'


class PostUpdateView(UpdateView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Пост успешно изменен'


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')