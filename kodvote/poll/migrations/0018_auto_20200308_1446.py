# Generated by Django 3.0.2 on 2020-03-08 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organize', '0001_initial'),
        ('poll', '0017_auto_20200308_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='poll',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organize.User'),
        ),
        migrations.AlterField(
            model_name='pollvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organize.User'),
        ),
    ]
