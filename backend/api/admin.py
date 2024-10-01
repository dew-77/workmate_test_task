from django.contrib import admin

from .models import Breed, Cat, Rating


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'color', 'owner')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_cat_count')
    search_fields = ('title',)

    def display_cat_count(self, obj):
        return Cat.objects.filter(breed=obj).count()

    display_cat_count.short_description = 'Кол-во котиков'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('who_rates', 'whom_rates', 'value')
    list_filter = ('who_rates', 'whom_rates', 'value')
