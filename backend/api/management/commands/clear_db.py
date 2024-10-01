from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Cat, Breed

User = get_user_model()


class Command(BaseCommand):
    help = 'Очистка ДБ от всех инстансов моделей'

    def handle(self, *args, **kwargs):
        Cat.objects.all().delete()

        Breed.objects.all().delete()

        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Удаление завершено.'))
