# Generated by Django 4.1.6 on 2023-03-24 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stream", "0007_alter_comment_author_alter_comment_contenttype"),
    ]

    operations = [
        migrations.RemoveField(model_name="comment", name="body",),
        migrations.RemoveField(model_name="comment", name="main_date",),
        migrations.RemoveField(model_name="comment", name="name",),
    ]
