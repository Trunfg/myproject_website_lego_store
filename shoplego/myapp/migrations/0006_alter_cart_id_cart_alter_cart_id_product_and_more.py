# Generated by Django 4.2.2 on 2024-04-03 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_product_img_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id_cart',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='id_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='myapp.user'),
        ),
        migrations.AlterField(
            model_name='history',
            name='id_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product'),
        ),
        migrations.AlterField(
            model_name='history',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='myapp.user'),
        ),
    ]