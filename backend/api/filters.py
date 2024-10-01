from django_filters import rest_framework as filters

from .models import Cat


class CatFilter(filters.FilterSet):
    breed = filters.CharFilter(
        field_name='breed__title',
        lookup_expr='icontains'
    )

    class Meta:
        model = Cat
        fields = ['breed']
