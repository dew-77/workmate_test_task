from colorfield.fields import ColorField
from django.db import IntegrityError
from rest_framework import serializers

from .models import Breed, Cat, Rating


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'title']


class CatSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    color = ColorField()

    class Meta:
        model = Cat
        fields = [
            'id', 'name', 'color', 'age',
            'breed', 'description', 'average_rating'
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'value', 'whom_rates']

    def validate_whom_rates(self, value):
        request = self.context['request']
        if value.owner == request.user:
            raise serializers.ValidationError(
                'Нельзя оценивать своего котика.')
        return value

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Вы уже оценили этого котика.')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method in ['GET']:
            representation['who_rates'] = instance.who_rates.id
        return representation
