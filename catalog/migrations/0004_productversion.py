# Generated by Django 5.0.4 on 2024-05-19 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_contacts"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductVersion",
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
                (
                    "version_number",
                    models.PositiveSmallIntegerField(verbose_name="Номер версии"),
                ),
                ("version_name", models.CharField(verbose_name="Название версии")),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, verbose_name="Признак текущей версии"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.product",
                        verbose_name="Продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "Версия",
                "verbose_name_plural": "Версии",
            },
        ),
    ]