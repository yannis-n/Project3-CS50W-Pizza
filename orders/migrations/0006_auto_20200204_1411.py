# Generated by Django 3.0.2 on 2020-02-04 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200204_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'ategories'},
        ),
        migrations.AlterField(
            model_name='menu_item',
            name='number_of_toppings',
            field=models.PositiveIntegerField(default=0),
        ),
    ]