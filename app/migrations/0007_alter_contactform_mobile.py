# Generated by Django 5.0.4 on 2024-05-26 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_contactform_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactform',
            name='mobile',
            field=models.CharField(max_length=14),
        ),
    ]
