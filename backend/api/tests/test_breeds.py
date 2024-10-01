import pytest
from api.models import Breed
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
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_get_breeds_list(api_client, create_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'testuser',
        'password': 'testpassword'
    })
    access_token = response.data['access']

    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    Breed.objects.create(title='Сиамская')
    Breed.objects.create(title='Персидская')

    url = reverse('api:breeds')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.data, list)

    assert len(response.data) > 0

    for breed in response.data:
        assert 'id' in breed
        assert 'title' in breed
        assert isinstance(breed['id'], int)
        assert isinstance(breed['title'], str)
