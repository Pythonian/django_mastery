# Generated by Django 4.1 on 2022-09-14 07:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0014_alter_candidate_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='experience',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='gender',
            field=models.CharField(default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='personality',
            field=models.CharField(choices=[('', 'Select a personality'), ('I am outgoing', 'I am outgoing'), ('I am antisocial', 'I am antisocial'), ('I am serious', 'I am serious')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='salary',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='smoker',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='', max_length=1),
        ),
    ]