# Generated by Django 5.0.4 on 2024-05-05 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval_app', '0004_alter_level_autumn_alter_level_spring_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peruser',
            name='phone',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
