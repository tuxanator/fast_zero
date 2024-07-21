from sqlalchemy import select

from fast_zero.models import User


def test_create_user_sql(session):
    # Usuário a ser enviado pra Session.
    user = User(username='gabriel', email='gabriel@test.com', password='senha')
    # Adiciona os dados na session.
    session.add(user)
    # Confirma e envia os dados para o Banco.
    session.commit()
    # Scalar() = Me traz um objeto Python.
    result = session.scalar(select(User).where(User.email == 'gabriel@test.com'))

    assert result.username == 'gabriel'
