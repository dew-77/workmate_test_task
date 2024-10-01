# Generated by Django 4.2.16 on 2024-09-30 22:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_alter_breed_title'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('who_rates', 'whom_rates')},
        ),
    ]
