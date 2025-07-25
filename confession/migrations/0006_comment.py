# Generated by Django 5.2.3 on 2025-07-25 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confession', '0005_confession_hearts'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('confession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='confession.confession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
