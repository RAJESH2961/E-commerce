# Generated by Django 5.0.4 on 2024-05-23 14:17

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='images/img-1.jpg', upload_to=app.models.getFileName),
        ),
    ]