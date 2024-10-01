# Тестовое задание компании Workmate
## Содержание

- [Доступ](#доступ)
- [Функциональность](#функциональность-api)
- [Установка и настройка](#установка-и-настройка)
  - [Docker](#docker)
  - [Ручной запуск (poetry)](#ручной-запуск-poetry)
- [Запуск тестов](#запуск-тестов)
- [Технологии](#технологии)

## Функциональность

Документация к API доступна после развертки проекта по адресу `127.0.0.1:8000/swagger/`.

Для наполнения БД данными реализована management-команда (см. раздел установки), данные с расширением `.csv` находятся в директории `backend/api/data`.

## Установка и настройка
Общие пункты для всех вариантов далее:
1. После клонирования проекта создайте файл .env и заполните по образцу .env.example:
```bash
ALLOWED_HOSTS="127.0.0.1 localhost"
DEBUG="True"

DB_NAME=workmate_db
DB_USER=postgres
DB_PASSWORD=somepassword
DB_HOST=db
DB_PORT=5432

POSTGRES_DB=workmate_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=DB_PASSWORD=somepassword
```
*рекомендую оставить параметр DEBUG в значении True, чтобы посмотреть документацию Swagger*

*для ручной развертки в параметр DB_HOST вписать localhost*

### Docker

2. Перейдите в директорию `gateway`:
```bash
cd gateway/
```
3. Запустите Docker Compose:
```bash
sudo docker compose up -d
```
4. После загрузки всех контейнеров выполните команды:
```bash
sudo docker exec gateway-backend-1 poetry run python manage.py migrate
sudo docker exec -it gateway-backend-1 poetry run python manage.py createsuperuser
sudo docker exec gateway-backend-1 poetry run python manage.py load_data
sudo docker exec gateway-backend-1 poetry run python manage.py collectstatic
```
5. Перейдите по адресу `127.0.0.1:8000/swagger/` для просмотра документации или воспользуйтесь утилитами для работы с API (например, Postman).

### Ручной запуск (poetry)
*Не забудьте создать базу данных PostgreSQL или раскомментировать блок с включением SQLite в `settings.py`.*
2. [Установите](https://python-poetry.org/docs/#installing-with-the-official-installer) `poetry` в вашу систему.
3. Выполните команды:
```bash
poetry install
cd backend
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py load_data
poetry run python manage.py collectstatic
poetry run python manage.py runserver
```

## Запуск тестов
```bash
cd backend/
poetry run pytest
```

## Технологии
- Python 3.12
- Poetry 1.8.3
- Django 4.2.16
- DRF 3.15.2 + SimpleJWT 5.3.1 + drf-yasg 1.21.7
- PostgreSQL 13
- pytest
- gunicorn
- Docker