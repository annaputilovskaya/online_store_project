# Generated by Django 4.2 on 2024-06-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_new_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="new_token",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
