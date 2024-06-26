from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Класс модели пользователя.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="Страна", **NULLABLE)
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)
    new_email = models.EmailField(
        verbose_name="Email",
        **NULLABLE,
        help_text="Для подтверждения изменения необходимо пройти по ссылке, направленной на email"
    )
    new_token = models.CharField(max_length=100, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
