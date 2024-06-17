from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from auth import hash_password

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def create_user(username: str, password: str):
    user = User(username=username, password_hash=password)
    session.add(user)
    session.commit()

def register_user(username, password, confirm_password):
    if password != confirm_password:
        return False, "Пароли не совпадают"

    hashed_password = hash_password(password)
    create_user(username, hashed_password)
    return True, f"Пользователь {username} успешно зарегистрирован"
