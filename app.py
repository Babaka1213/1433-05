import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from getpass import getpass

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def create_user(username: str, password: str):
    user = User(username=username, password_hash=password)
    session.add(user)
    session.commit()

def hash_password(password: str) -> str:
    # Ваша логика хэширования пароля
    return password

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        messagebox.showerror("Ошибка", "Пароли не совпадают")
        return

    hashed_password = hash_password(password)
    create_user(username, hashed_password)
    messagebox.showinfo("Успех", f"Пользователь {username} успешно зарегистрирован")

def main():
    global username_entry, password_entry, confirm_password_entry

    root = tk.Tk()
    root.title("Регистрация пользователя")

    username_label = tk.Label(root, text="Имя пользователя:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    confirm_password_label = tk.Label(root, text="Подтвердите пароль:")
    confirm_password_label.pack()
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack()

    register_button = tk.Button(root, text="Зарегистрировать", command=register_user)
    register_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
