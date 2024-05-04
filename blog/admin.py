from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'is_published')
    list_filter = ('created_at', 'is_published')
