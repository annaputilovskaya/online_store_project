# Generated by Django 4.2 on 2024-05-26 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0004_productversion"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
    ]