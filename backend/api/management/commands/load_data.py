import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Cat, Breed

User = get_user_model()


class Command(BaseCommand):
    help = 'Загрузка данных из CSV-файлов в БД'

    def handle(self, *args, **kwargs):
        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        data_dir = os.path.join(project_root, '..', 'data')

        users_file = os.path.join(data_dir, 'users.csv')
        breeds_file = os.path.join(data_dir, 'breeds.csv')
        cats_file = os.path.join(data_dir, 'cats.csv')

        self.create_users_from_csv(users_file)
        self.create_breeds_from_csv(breeds_file)
        self.create_cats_from_csv(cats_file)

        self.stdout.write(self.style.SUCCESS('Загрузка завершена.'))

    def create_users_from_csv(self, filepath):
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.create_user(
                    username=row['username'], password=row['password']
                )

    def create_breeds_from_csv(self, filepath):
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Breed.objects.create(title=row['title'])

    def create_cats_from_csv(self, filepath):
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                owner = User.objects.get(username=row['owner_username'])
                breed = Breed.objects.get(title=row['breed_title'])

                Cat.objects.create(
                    name=row['name'],
                    age=int(row['age']),
                    color=row['color'],
                    breed=breed,
                    description=row['description'],
                    owner=owner
                )
