from django.db import models
from django.db.models import CASCADE

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='catalog/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', **NULLABLE,
                                 verbose_name='Категория')
    price = models.PositiveIntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    owner = models.ForeignKey(User, verbose_name='Владелец', **NULLABLE, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        permissions = [
            ('change_category', 'Can change category'),
            ('change_description', 'Can change product description'),
            ('cancel_publication', 'Can cancel publication of product'),
        ]


class Contacts(models.Model):
    country = models.CharField(max_length=50, verbose_name='Страна')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    inn = models.PositiveBigIntegerField(verbose_name='ИНН')

    def __str__(self):
        return f'{self.country}, {self.address}. ИНН: {self.inn}'

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class ProductVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE, verbose_name='Продукт')
    version_number = models.PositiveSmallIntegerField(verbose_name='Номер версии')
    version_name = models.CharField(verbose_name='Название версии')
    is_active = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.version_number} ({self.version_name})'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
