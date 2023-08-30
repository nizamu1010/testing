# Generated by Django 4.2.3 on 2023-07-21 17:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posting", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="shares",
        ),
        migrations.RemoveField(
            model_name="post",
            name="likers",
        ),
        migrations.AddField(
            model_name="post",
            name="likers",
            field=models.ManyToManyField(
                related_name="liked_posts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
