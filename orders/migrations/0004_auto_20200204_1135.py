# Generated by Django 3.0.2 on 2020-02-04 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200204_1057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu_item',
            old_name='large',
            new_name='large_price',
        ),
        migrations.RenameField(
            model_name='menu_item',
            old_name='one_size',
            new_name='one_size_price',
        ),
        migrations.RenameField(
            model_name='menu_item',
            old_name='small',
            new_name='small_price',
        ),
    ]
