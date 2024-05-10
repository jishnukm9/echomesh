# Generated by Django 5.0.1 on 2024-01-28 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_userprofile_cover_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='relationship_status',
            field=models.CharField(choices=[('Single', 'Single'), ('In a relationship', 'In a relationship'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Engaged', 'Engaged')], default='Single', max_length=20),
        ),
    ]
