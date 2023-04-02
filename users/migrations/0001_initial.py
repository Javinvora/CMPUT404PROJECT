# Generated by Django 4.1.7 on 2023-04-02 02:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('summary', models.CharField(blank=True, max_length=500, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('host', models.CharField(default='localhost:8000/', max_length=100)),
                ('displayName', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=100)),
                ('github', models.CharField(blank=True, max_length=100, null=True)),
                ('profileImage', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('follows', models.ManyToManyField(blank=True, related_name='followed_by', to='users.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_requests', models.ManyToManyField(related_name='recipient_inboxes', to='users.friendrequest')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox', to='users.profile')),
            ],
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor', to='users.profile'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object', to='users.profile'),
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(related_name='user_follower', to='users.profile')),
            ],
        ),
    ]
