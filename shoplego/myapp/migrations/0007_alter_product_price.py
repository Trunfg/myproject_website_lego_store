# Generated by Django 5.0.3 on 2024-04-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_cart_id_cart_alter_cart_id_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.TextField(),
        ),
    ]
