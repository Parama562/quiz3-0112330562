import os

import pytest
import requests

BASE_URL = os.environ.get('BOOK_API_BASE_URL', 'http://localhost:8000')


@pytest.fixture(autouse=True)
def clean_books():
    # Run only against the quiz's disposable in-memory server.
    response = requests.get(f'{BASE_URL}/books', timeout=5)
    response.raise_for_status()
    for book_id in response.json():
        response = requests.delete(f'{BASE_URL}/books/{book_id}', timeout=5)
        assert response.status_code == 200
    yield


def create_book(title='Clean Code'):
    response = requests.post(f'{BASE_URL}/books', json={
        'title': title, 'author': 'Robert Martin', 'price': 29.99,
    }, timeout=5)
    assert response.status_code == 201
    return response


def test_create_book():
    response = create_book()
    assert response.status_code == 201
    assert response.json()['title'] == 'Clean Code'


def test_delete_book():
    created = create_book('Test Book')
    book_id = created.json()['id']
    response = requests.delete(f'{BASE_URL}/books/{book_id}', timeout=5)
    assert response.status_code == 200
    check = requests.get(f'{BASE_URL}/books', timeout=5)
    assert check.status_code == 200
    assert len(check.json()) == 0


def test_get_all_books():
    create_book('Book One')
    create_book('Book Two')
    response = requests.get(f'{BASE_URL}/books', timeout=5)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_book():
    created = create_book()
    book_id = created.json()['id']
    response = requests.put(f'{BASE_URL}/books/{book_id}',
                            json={'price': 39.99}, timeout=5)
    assert response.status_code == 200
    assert response.json()['price'] == 39.99
    assert response.json()['title'] == 'Clean Code'
    stored = requests.get(f'{BASE_URL}/books', timeout=5).json()[str(book_id)]
    assert stored['price'] == 39.99
