# Generated by Django 5.2.3 on 2025-07-25 20:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_remove_journal_date_journal_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
