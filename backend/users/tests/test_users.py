from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


def create_expired_token(user):
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=timedelta(seconds=-1))
    return str(token)


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
def test_successful_authentication(api_client, create_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'testuser',
        'password': 'testpassword'
    })

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_failed_authentication(api_client):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'invaliduser',
        'password': 'invalidpassword'
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_access_with_token(api_client, create_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'testuser',
        'password': 'testpassword'
    })
    access_token = response.data['access']

    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    cats_url = reverse('api:cat-list')
    response = api_client.get(cats_url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_access_with_expired_token(api_client, create_user):
    expired_token = create_expired_token(create_user)

    cats_url = reverse('api:cat-list')
    response = api_client.get(
        cats_url, HTTP_AUTHORIZATION=f'Bearer {expired_token}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_access_with_invalid_token(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalidtoken')

    cats_url = reverse('api:cat-list')
    response = api_client.get(cats_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
