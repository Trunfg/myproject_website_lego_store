# Generated by Django 5.0.3 on 2024-03-31 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(default='khach_hang', max_length=20),
        ),
    ]