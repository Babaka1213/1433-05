import pytest
from auth import hash_password, check_password

def test_hash_password():
    hashed_password = hash_password("test_password")
    assert hashed_password is not None

def test_check_password():
    hashed_password = hash_password("test_password")
    assert check_password("test_password", hashed_password)
    assert not check_password("wrong_password", hashed_password)
