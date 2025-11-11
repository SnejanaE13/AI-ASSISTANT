from app.db import models, schemas, CRUD
import bcrypt


def test_user_crud(db):
    user_data = schemas.UserCreate(
        email="test@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
        role="student"
    )

    #creating user
    created_user = CRUD.create_user(db, user_data)
    assert created_user.email == user_data.email

    #get user via email
    fetched_user = CRUD.get_user_by_email(db, user_data.email)
    assert fetched_user is not None
    assert fetched_user.email == user_data.email

    #get user via id
    fetched_user = CRUD.get_user(db, created_user.user_id)
    assert fetched_user is not None
    assert fetched_user.user_id == created_user.user_id
    assert fetched_user.email == created_user.email

def test_verify_password(db):
    user_data = schemas.UserCreate(
        email="secure@example.com",
        password="newpassword123",
        first_name="Fred",
        last_name="Smith",
        role="teacher"
    )

    created_user = CRUD.create_user(db, user_data)
    stored_hash = created_user.password_hash.decode() if isinstance(created_user.password_hash, bytes) else created_user.password_hash

    assert bcrypt.checkpw(user_data.password.encode('utf-8'), stored_hash.encode("utf-8"))







