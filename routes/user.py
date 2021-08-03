from fastapi import APIRouter
from starlette.responses import Response
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT

# For cipher passwords.
# This isn't the best way
# to encrypt passwords!
key = Fernet.generate_key()
cipher = Fernet(key)

user = APIRouter()

@user.get('/users')
def get_users():
    #.select() returns a db cursor
    return conn.execute(users.select()).fetchall()

@user.post('/users')
def insert_user(user: User):
    new_user = { "name": user.name, "email": user.email }
    new_user['password'] = cipher.encrypt(user.password.encode('utf-8'))
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get('/users/{id}')
def get_single_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.delete('/users/{id}')
def delete_single_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put('/users/{id}')
def update_single_user(id: str, user: User):
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=cipher.encrypt(user.password.encode('utf-8'))
        ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()
