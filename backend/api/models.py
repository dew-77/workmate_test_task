from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from backend.constants import (BREED_TITLE_MAX_LENGTH,
                               CAT_DESCRIPTION_MAX_LENGTH, CAT_NAME_MAX_LENGTH)

User = get_user_model()


class Breed(models.Model):
    title = models.CharField(
        'Название',
        max_length=BREED_TITLE_MAX_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'породы'

    def __str__(self):
        return self.title


class Cat(models.Model):
    name = models.CharField('Имя', max_length=CAT_NAME_MAX_LENGTH)
    age = models.PositiveIntegerField('Возраст (месяцев)', null=False)
    color = ColorField('Цвет', null=False, blank=False)
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        related_name='cats',
        on_delete=models.CASCADE
    )
    breed = models.ForeignKey(
        Breed,
        verbose_name='Порода',
        on_delete=models.CASCADE,
        related_name='cats',
    )
    description = models.TextField(
        'Описание',
        max_length=CAT_DESCRIPTION_MAX_LENGTH,
        blank=True,
    )

    def average_rating(self):
        return self.ratings.aggregate(
            models.Avg('value'))['value__avg'] or 0

    class Meta:
        verbose_name = 'Котик'
        verbose_name_plural = 'котики'

    def __str__(self):
        return f'{self.name}'


class Rating(models.Model):
    value = models.PositiveIntegerField(
        'Значение оценки',
        validators=[
            MinValueValidator(1, message='Оценка должна быть >= 1'),
            MaxValueValidator(5, message='Оценка должна быть <= 5')
        ]
    )
    who_rates = models.ForeignKey(
        User,
        verbose_name='Оценил',
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    whom_rates = models.ForeignKey(
        Cat,
        verbose_name='Оцененный',
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'оценки'
        unique_together = ('who_rates', 'whom_rates')

    def __str__(self):
        return f'Оценка {self.value} от {self.who_rates} для {self.whom_rates}'
