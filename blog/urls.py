from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = BlogConfig.name


urlpatterns = (
    path('', PostListView.as_view(), name='post_list'),
    path('view/<int:pk>/', PostDetailView.as_view(), name='view'),
    path('blog/create/', PostCreateView.as_view(), name='create'),
    path('blog/<int:pk>/edit/', PostUpdateView.as_view(), name='edit'),
    path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='delete'),
)
