# Generated by Django 3.0.2 on 2020-02-04 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200204_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu_item',
            name='price',
        ),
        migrations.AddField(
            model_name='menu_item',
            name='large',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='menu_item',
            name='one_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='menu_item',
            name='small',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]