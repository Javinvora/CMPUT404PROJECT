# Generated by Django 4.1.6 on 2023-03-22 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0002_post_categories_post_comments_post_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
    ]
