# Generated by Django 4.2.16 on 2024-09-30 19:46

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=12, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Порода',
                'verbose_name_plural': 'породы',
            },
        ),
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Имя')),
                ('age', models.PositiveIntegerField(verbose_name='Возраст (месяцев)')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None, verbose_name='Цвет')),
                ('description', models.TextField(blank=True, max_length=120, verbose_name='Описание')),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cats', to='api.breed', verbose_name='Порода')),
            ],
            options={
                'verbose_name': 'Котик',
                'verbose_name_plural': 'котики',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Оценка должна быть >= 1'), django.core.validators.MaxValueValidator(5, message='Оценка должна быть <= 5')], verbose_name='Значение оценки')),
                ('who_rates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL, verbose_name='Оценил')),
                ('whom_rates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api.cat', verbose_name='Оцененный')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'оценки',
            },
        ),
    ]
