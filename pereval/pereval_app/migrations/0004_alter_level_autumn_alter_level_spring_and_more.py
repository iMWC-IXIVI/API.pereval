# Generated by Django 5.0.4 on 2024-05-05 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval_app', '0003_alter_pereval_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='autumn',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='spring',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='summer',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='winter',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='pereval',
            name='status',
            field=models.CharField(default='new', max_length=10),
        ),
    ]