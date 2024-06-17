from auth import hash_password, check_password
from db import create_user, get_user_by_username, update_user_password
from models import User

def register_user(username, password):
    hashed_password = hash_password(password)
    user = create_user(username, hashed_password)
    if user:
        print(f"Пользователь {username} успешно зарегистрирован.")
    else:
        print(f"Ошибка при регистрации пользователя {username}.")

def login_user(username, password):
    user = get_user_by_username(username)
    if user and check_password(password, user.password_hash):
        print(f"Пользователь {username} успешно авторизован.")
    else:
        print(f"Неверные имя пользователя или пароль для пользователя {username}.")

if __name__ == "__main__":
    # Пример использования:
    register_user("user1", "password123")
    login_user("user1", "password123")

