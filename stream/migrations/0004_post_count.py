# Generated by Django 4.1.6 on 2023-03-27 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stream", "0003_remove_comment_main_post_remove_post_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post", name="count", field=models.IntegerField(default=0),
        ),
    ]
