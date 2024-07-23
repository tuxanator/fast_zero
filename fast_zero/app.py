from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/', response_model=Message)
def read_root(session: Session = Depends(get_session)):  # Definindo o tipo de session.
    return {'Message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    # faz uma query no banco e armazena o resultado em db_user.
    db_user = session.scalar(
        select(User).where((User.username == user.username) or (User.email == user.email))
    )
    # checa se o usuário já está cadastrado no banco.
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Username already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists')
    # cria o usuário no banco de acordo com schema definido do pydantic.
    db_user = User(username=user.username, email=user.email, password=user.password)
    # adiciona o usuário na session.
    session.add(db_user)
    # confirma os dados do usuário.
    session.commit()
    """atualiza o usuário no banco para que ele tenha um ID
         para ser retornado pelo schema UserPublic."""
    session.refresh(db_user)
    # retorna o usuário no schema de UserPublic.
    return db_user


@app.get('/users/', response_model=UserList)
def read_users(session: Session = Depends(get_session), limit: int = 10, skip: int = 0):
    users_db = session.scalars(select(User).limit(limit).offset(skip)).all()

    return {'users': users_db}


@app.put('/users/{user_id}', status_code=HTTPStatus.ACCEPTED, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'Message': 'User deleted'}


# Implementação da rota get que obtém '/users/{user_id}'
@app.get('/users/{user_id}', response_model=UserPublic)
def read_specific_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return db_user
