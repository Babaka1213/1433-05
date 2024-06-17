import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth import check_password, hash_password
from registration_app import open_registration_window
from chat_app import ChatApp
from models import Base, User, Message

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц базы данных, если они еще не созданы
Base.metadata.create_all(bind=engine)

def login_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()

    if user and check_password(password, user.password_hash):
        root.destroy()  # Закрываем окно входа
        chat_root = tk.Tk()
        chat_app = ChatApp(chat_root, username=username)
        chat_root.mainloop()
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

def main():
    global root

    root = tk.Tk()
    root.title("Вход в систему")

    username_label = tk.Label(root, text="Имя пользователя:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    login_button = tk.Button(root, text="Вход", command=lambda: login_user(username_entry.get(), password_entry.get()))
    login_button.pack()

    register_button = tk.Button(root, text="Регистрация", command=open_registration_window)
    register_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
