import pytest
from db import create_user, get_user_by_username, update_user_password

@pytest.fixture
def add_user():
    username = "test_user"
    password_hash = "hashed_password"
    return create_user(username, password_hash)

def test_create_user(add_user):
    assert add_user.username == "test_user"

def test_get_user_by_username(add_user):
    user = get_user_by_username("test_user")
    assert user is not None
    assert user.username == "test_user"

def test_update_user_password(add_user):
    assert update_user_password("test_user", "new_hashed_password")
    user = get_user_by_username("test_user")
    assert user.password_hash == "new_hashed_password"
