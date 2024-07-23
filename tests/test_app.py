from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(  # recebe um UserSchema
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test_email@test.com',
            'password': 'senha',
        },
    )
    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Valida o UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'test_email@test.com',
        'id': 1,
    }


def test_create_user_404_username(client, user):
    response = client.post(
        '/users/', json={'username': 'test', 'email': 'test@test.com', 'password': 'senha123'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_404_email(client, user):
    response = client.post(
        '/users/', json={'username': 'test1', 'email': 'test@test.com', 'password': 'senha123'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# teste do exercício de CRUD
def test_read_specific_user(client, user):
    response = client.get('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
    }


def test_read_specific_user_404(client, user):
    response = client.get('/users/2/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1/',
        json={'username': 'teste2', 'email': 'test@test.com', 'password': 'senha'},
    )

    assert response.status_code == HTTPStatus.ACCEPTED


def test_update_user_404(client, user):
    response = client.put(
        '/users/5/',
        json={'username': 'teste2', 'email': 'test@test.com', 'password': 'senha', 'id': 1},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1/')

    assert response.json() == {'Message': 'User deleted'}


def test_delete_user_404(client, user):
    response = client.delete('/users/5/')

    assert response.status_code == HTTPStatus.NOT_FOUND
