# Generated by Django 3.0.2 on 2020-03-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0040_auto_20200310_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollchoice',
            name='image',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
