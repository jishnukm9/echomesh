# Generated by Django 5.0.1 on 2024-02-01 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sublike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_commentlikes', to='core.comment'),
        ),
    ]