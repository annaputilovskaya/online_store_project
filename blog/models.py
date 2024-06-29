from django.db import models

NULLABLE = {"blank": True, "null": True}


class Post(models.Model):
    """
    Модель статьи блога.
    """

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(max_length=150, verbose_name="slug", **NULLABLE)
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="blog/", verbose_name="Изображение", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
