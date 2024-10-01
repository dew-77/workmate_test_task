import pytest
from api.models import Breed, Cat
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword'
    )
    return user


@pytest.fixture
def api_client(create_user):
    from rest_framework.test import APIClient
    user = create_user

    client = APIClient()

    url = reverse('token_obtain_pair')
    response = client.post(url, {
        'username': user.username,
        'password': 'testpassword'
    })

    assert response.status_code == status.HTTP_200_OK
    access_token = response.data.get('access')

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    return client


@pytest.fixture
def create_breeds(db):
    Breed.objects.create(title='Сиамская')
    Breed.objects.create(title='Персидская')


@pytest.fixture
def create_cats(db, create_breeds, create_user):
    user = create_user

    cat1 = Cat.objects.create(
        name='Артемка',
        color='#FFFFFF',
        breed=Breed.objects.get(title='Сиамская'),
        description='Супер котик, работящий, умный и красивый',
        owner=user,
        age=2
    )
    Cat.objects.create(
        name='Абобус',
        color='#FFFFFF',
        breed=Breed.objects.get(title='Персидская'),
        description='ну просто абобус',
        owner=user,
        age=3
    )
    return cat1


@pytest.mark.django_db
def test_add_cat(api_client, create_breeds, create_user):
    url = reverse('api:cat-list')

    data = {
        'name': 'Мурзик',
        'color': '#FFFFFF',
        'breed': Breed.objects.get(title='Сиамская').id,
        'description': 'Классный кот',
        'age': 1
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Cat.objects.filter(name='Мурзик').exists()


@pytest.mark.django_db
def test_add_cat_invalid_data(api_client):
    url = reverse('api:cat-list')

    invalid_data = {
        'name': '',
        'color': '#31313131',
        'breed': 999,
        'description': 'Не кот (хахах)',
        'age': -1
    }
    response = api_client.post(url, invalid_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'breed' in response.data
    assert 'name' in response.data
    assert 'age' in response.data


@pytest.mark.django_db
def test_update_cat(api_client, create_cats, create_user):
    cat_id = create_cats.id
    url = reverse('api:cat-detail', args=[cat_id])
    updated_data = {
        'name': 'неАртемка',
        'color': '#113411',
        'breed': create_cats.breed.id,
        'description': 'Новый кот уря!',
        'age': 3
    }
    response = api_client.put(url, updated_data)
    assert response.status_code == status.HTTP_200_OK
    create_cats.refresh_from_db()
    assert create_cats.name == 'неАртемка'


@pytest.mark.django_db
def test_update_cat_invalid_data(api_client, create_cats):
    cat_id = create_cats.id
    url = reverse('api:cat-detail', args=[cat_id])

    invalid_data = {
        'name': '',
        'color': '#231312313131',
        'breed': 999,
        'description': 'Не кот',
        'age': -1
    }
    response = api_client.put(url, invalid_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'breed' in response.data
    assert 'name' in response.data
    assert 'age' in response.data


@pytest.mark.django_db
def test_update_nonexistent_cat(api_client):
    url = reverse('api:cat-detail', args=[999])
    updated_data = {
        'name': 'Погроммист',
        'color': '#131332',
        'breed': 1,
        'description': 'Новый кот',
        'age': 3
    }
    response = api_client.put(url, updated_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_cat(api_client, create_cats):
    cat_id = create_cats.id
    url = reverse('api:cat-detail', args=[cat_id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Cat.objects.filter(id=cat_id).exists()


@pytest.mark.django_db
def test_delete_nonexistent_cat(api_client):
    url = reverse('api:cat-detail', args=[999])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_owner_cannot_delete_others_cats(api_client, create_cats):
    User.objects.create_user(
        username='another_user',
        password='another_password'
    )
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'another_user',
        'password': 'another_password'
    })

    assert response.status_code == status.HTTP_200_OK

    access_token = response.data.get('access')
    api_client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + access_token)

    url = reverse('api:cat-detail', args=[create_cats.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_owner_cannot_update_others_cats(api_client, create_cats):
    User.objects.create_user(
        username='another_user',
        password='another_password'
    )
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'another_user',
        'password': 'another_password'
    })

    assert response.status_code == status.HTTP_200_OK

    access_token = response.data.get('access')
    api_client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + access_token)

    url = reverse('api:cat-detail', args=[create_cats.id])

    updated_data = {
        'name': 'Новый',
        'color': '#121212',
        'breed': create_cats.breed.id,
        'description': 'Новый кэт',
        'age': 3
    }
    response = api_client.put(url, updated_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
