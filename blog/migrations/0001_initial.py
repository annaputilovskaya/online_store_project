# Generated by Django 5.0.4 on 2024-05-04 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="slug"
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Опубликовано"),
                ),
                (
                    "views_count",
                    models.IntegerField(default=0, verbose_name="Просмотры"),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
            },
        ),
    ]