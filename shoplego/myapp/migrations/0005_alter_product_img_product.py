# Generated by Django 5.0.3 on 2024-04-01 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_user_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img_product',
            field=models.ImageField(default=None, upload_to='product_images/'),
        ),
    ]