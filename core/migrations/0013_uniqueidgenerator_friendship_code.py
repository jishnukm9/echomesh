# Generated by Django 5.0.1 on 2024-02-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_subcomments_comment_text_alter_subcomments_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueIdGenerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=200, unique=True)),
                ('prefix', models.CharField(max_length=200, unique=True)),
                ('uniqueid', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='code',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]