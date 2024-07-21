from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'senha',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Valida o UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'testusername', 'email': 'test@test.com', 'id': 1}]
    }


# teste do exercício do CRUD
def test_read_specific_user(client):
    response = client.get('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': {
            'id': 1,
            'username': 'testusername',
            'email': 'test@test.com',
        }
    }


def test_update_user(client):
    response = client.put(
        '/users/1/',
        json={'username': 'teste2', 'email': 'test@test.com', 'password': 'senha', 'id': 1},
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_404(client):
    response = client.put(
        '/users/0/',
        json={'username': 'teste2', 'email': 'test@test.com', 'password': 'senha', 'id': 1},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1/')

    assert response.json() == {'Message': 'User deleted'}


def test_delete_user_404(client):
    response = client.delete('/users/0/')

    assert response.status_code == HTTPStatus.NOT_FOUND
