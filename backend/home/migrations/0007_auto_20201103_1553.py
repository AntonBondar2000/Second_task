# Generated by Django 2.2 on 2020-11-03 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201103_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.ImageField(upload_to='img/', verbose_name='Фотография'),
        ),
    ]
