# Generated by Django 4.1.4 on 2023-02-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0009_products_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image5',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
