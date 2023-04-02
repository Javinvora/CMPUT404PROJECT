# Generated by Django 4.1.7 on 2023-04-02 02:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment', models.TextField()),
                ('contentType', models.TextField(default='type placeholder')),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=100)),
                ('origin', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('contentType', models.CharField(blank=True, max_length=150, null=True)),
                ('content', models.TextField()),
                ('categories', models.CharField(blank=True, max_length=50, null=True)),
                ('count', models.IntegerField(default=0)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/post_photo')),
                ('visibility', models.CharField(blank=True, max_length=150, null=True)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('comments', models.ManyToManyField(blank=True, to='stream.comment')),
            ],
        ),
    ]