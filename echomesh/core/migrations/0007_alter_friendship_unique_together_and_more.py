# Generated by Django 5.0.1 on 2024-01-28 15:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_post_feeling_alter_post_image_alter_post_text_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together={('sender', 'receiver')},
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('post', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='save',
            unique_together={('post', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='share',
            unique_together={('post', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='sublike',
            unique_together={('comment', 'user')},
        ),
    ]
