# Generated by Django 3.0.2 on 2020-03-10 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0042_auto_20200311_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='picture',
            field=models.ImageField(upload_to='media/'),
        ),
    ]