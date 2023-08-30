# Generated by Django 4.2.3 on 2023-07-24 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("posting", "0004_alter_comment_comment_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="parent_comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="posting.comment",
            ),
        ),
    ]