# Generated by Django 4.2.9 on 2024-02-06 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_uniqueidgenerator_friendship_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='chatDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('roomname', models.CharField(max_length=200)),
                ('userid', models.IntegerField()),
                ('userimage', models.URLField(max_length=2000)),
                ('userfullname', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
