# Generated by Django 3.0.2 on 2020-02-04 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0004_auto_20200204_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_item',
            name='number_of_toppings',
            field=models.PositiveIntegerField(),
        ),
        migrations.CreateModel(
            name='Shopping_Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Menu_Item')),
                ('toppings', models.ManyToManyField(blank=True, to='orders.Topping')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
