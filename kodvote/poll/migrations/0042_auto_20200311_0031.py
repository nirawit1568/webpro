# Generated by Django 3.0.2 on 2020-03-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0041_pollchoice_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='picture',
            field=models.CharField(max_length=50),
        ),
    ]
