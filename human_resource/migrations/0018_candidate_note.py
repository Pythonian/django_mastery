# Generated by Django 4.1 on 2022-09-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0017_candidate_databases_candidate_frameworks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]