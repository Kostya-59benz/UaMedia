# Generated by Django 3.2.14 on 2022-11-19 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uaMedia', '0002_auto_20221030_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='Null', verbose_name='Описание'),
        ),
    ]