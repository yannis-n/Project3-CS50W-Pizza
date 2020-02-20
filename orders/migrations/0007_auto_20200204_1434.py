# Generated by Django 3.0.2 on 2020-02-04 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_auto_20200204_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shopping_Cart_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.PositiveIntegerField()),
                ('size', models.CharField(choices=[('small', 'small'), ('large', 'large'), ('one size', 'one size')], max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Menu_Item')),
                ('toppings', models.ManyToManyField(blank=True, to='orders.Topping')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.DeleteModel(
            name='Shopping_Cart',
        ),
    ]
