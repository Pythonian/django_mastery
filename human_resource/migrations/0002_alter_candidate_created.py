# Generated by Django 4.1 on 2023-03-20 16:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]