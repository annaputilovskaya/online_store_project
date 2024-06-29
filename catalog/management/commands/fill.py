import json

from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """
        Считывает категории из json-файла и создает список словарей.
        :return: Список словарей с категориями
        """
        with open("catalog_data.json") as file:
            catalog_json = json.load(file)
            categories_list = []
            for item in catalog_json:
                if item.get("model") == "catalog.category":
                    category_dict = item.get("fields")
                    category_dict["pk"] = item.get("pk")
                    categories_list.append(category_dict)
            return categories_list

    @staticmethod
    def json_read_products():
        """
        Считывает продукты из json-файла и создает список словарей.
        :return: Список словарей с продуктами
        """
        with open("catalog_data.json") as file:
            catalog_json = json.load(file)
            products_list = []
            for item in catalog_json:
                if item.get("model") == "catalog.product":
                    products_list.append(item.get("fields"))
            return products_list

    def handle(self, *args, **options):
        """
        Обработка команды: удаление всех существующих данных из базы
        и занесение новых из json-файла.
        """

        # Удаление данных
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;")
        Product.objects.all().delete()
        Category.objects.all().delete()
        # sqlsequencereset

        # Создание списков для хранения объектов
        product_for_create = []
        category_for_create = []

        # Добавление информации о категориях в список
        for category in Command.json_read_categories():
            category_for_create.append(Category(**category))

        # Создание объектов "категория" в базе
        Category.objects.bulk_create(category_for_create)

        # Добавление информации о продуктах в список
        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    name=product["name"],
                    description=product["description"],
                    image=product["image"],
                    category=Category.objects.get(pk=product["category"]),
                    price=product["price"],
                    created_at=product["created_at"],
                    updated_at=product["updated_at"],
                )
            )

        # Создаем объекты "продукт" в базе
        Product.objects.bulk_create(product_for_create)
