# Generated by Django 3.0.2 on 2020-03-07 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organize', '0001_initial'),
        ('poll', '0009_auto_20200307_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='users',
        ),
        migrations.AlterField(
            model_name='poll',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organize.user'),
        ),
    ]
