from app.models import connect_db
import pytest
from .conftest import client



@pytest.fixture(scope='module')
def temp_db():
    yield connect_db()


def test_registration_for_users(temp_db):
    response = client.post('/registration', data={
        "username": 'user1',
        "password": "parol1",
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "35",
        "position": "Менеджер"
    })
    assert response.status_code == 200


def test_update_user_post(temp_db):
    response = client.post('/update_user_post', data={
        "username": 'user1',
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "37",
        "position": "Менеджер"
    })
    assert response.status_code == 200


def test_delete_user_post(temp_db):
    response = client.post('/delete_user_post', data={
        "username": 'user1'
    })
    assert response.status_code == 200


def test_add_information_about_salary_post(temp_db):
    response = client.post('/add_information_about_salary', data={
        "username": 'user1',
        "salary": "37589.45",
        "salary_increase_date": "29.11.23"
    })
    assert response.status_code == 200


def test_update_salary_post(temp_db):
    response = client.post('/update_info_about_salary_post', data={
        "username": 'user1',
        "salary": "39589.45",
        "salary_increase_date": "17.12.23"
    })
    assert response.status_code == 200


def test_delete_salary_post(temp_db):
    response = client.post('/delete_salary_post', data={
        "username": 'user1'
    })
    assert response.status_code == 200


def test_login_for_access_token():
    client.post('/registration', data={
        "username": 'user1',
        "password": 'parol1',
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "35",
        "position": "Менеджер"
    })

    response = client.post('/token', data={
        'username': "user1",
        'password': 'parol1'
    })
    assert response.status_code == 200


def test_index():
    response = client.get('/')
    assert response.status_code == 200


def test_auth_for_users():
    response = client.get('/login_for_users')
    assert response.status_code == 200


def test_add_information_about_salary_get():
    client.post('/registration', data={
        "username": 'user1',
        "password": 'parol1',
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "35",
        "position": "Менеджер"
    })

    client.post('/token', data={
        'username': "user1",
        'password': 'parol1'
    })
    response = client.get('/add_info_about_salary')
    assert response.status_code == 200


def test_update_salary():
    client.post('/registration', data={
        "username": 'user1',
        "password": 'parol1',
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "35",
        "position": "Менеджер"
    })

    client.post('/token', data={
        'username': "user1",
        'password': 'parol1'
    })
    response = client.get('/update_info_about_salary')
    assert response.status_code == 200


def test_delete_salary():
    client.post('/registration', data={
        "username": 'user1',
        "password": 'parol1',
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "35",
        "position": "Менеджер"
    })

    client.post('/token', data={
        'username': "user1",
        'password': 'parol1'
    })
    response = client.get('/delete_salary')
    assert response.status_code == 200


def test_get_info():
    client.post('/registration', data={
        "username": 'user1',
        "password": 'parol1',
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "35",
        "position": "Менеджер"
    })

    client.post('/token', data={
        'username': "user1",
        'password': 'parol1'
    })
    response = client.get('/get_info')
    assert response.status_code == 200


def test_get_users():
    response = client.get('/get_users')
    assert response.status_code == 200


def test_get_salary_list():
    response = client.get('/get_salary_list')
    assert response.status_code == 200


def test_get_info_about_salay():
    client.post('/registration', data={
        "username": 'user1',
        "password": 'parol1',
        "permission_level": "1",
        "full_name": "Петров Владимир Иванович",
        "age": "35",
        "position": "Менеджер"
    })

    client.post('/token', data={
        'username': "user1",
        'password': 'parol1'
    })

    client.post('/add_information_about_salary', data={
        "username": "user1",
        "salary": "39578.43",
        "salary_increase_date": "27.10.23"
    })

    response = client.post("/get_info_about_salary")
    assert response.status_code == 200

