import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def authenticate_user(username: str, password: str) -> bool:
    user = session.query(User).filter(User.username == username).first()
    if user and user.password_hash == password:
        return True
    else:
        return False

def show_message_window(message):
    message_window = tk.Toplevel(root)
    message_window.title("Сообщение")

    message_label = tk.Label(message_window, text=message, padx=20, pady=20)
    message_label.pack()

    ok_button = tk.Button(message_window, text="OK", command=message_window.destroy)
    ok_button.pack()

def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        show_message_window("Введите имя пользователя и пароль")
        return

    if authenticate_user(username, password):
        show_message_window("Вход выполнен успешно")
        # Здесь можете добавить логику для перехода в главное окно приложения
    else:
        show_message_window("Неверное имя пользователя или пароль")

def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Регистрация пользователя")

    def register_user():
        username_reg = username_entry_reg.get()
        password_reg = password_entry_reg.get()
        confirm_password_reg = confirm_password_entry_reg.get()

        if not username_reg or not password_reg or not confirm_password_reg:
            show_message_window("Заполните все поля")
            return

        # Проверка наличия пользователя с таким же именем
        user_check = session.query(User).filter(User.username == username_reg).first()
        if user_check:
            show_message_window("Пользователь с таким именем уже существует")
            return

        if password_reg != confirm_password_reg:
            show_message_window("Пароли не совпадают")
            return

        # Создание нового пользователя
        new_user = User(username=username_reg, password_hash=password_reg)
        session.add(new_user)
        session.commit()

        show_message_window("Пользователь зарегистрирован успешно")
        registration_window.destroy()

    username_label_reg = tk.Label(registration_window, text="Имя пользователя:")
    username_label_reg.pack()
    username_entry_reg = tk.Entry(registration_window)
    username_entry_reg.pack()

    password_label_reg = tk.Label(registration_window, text="Пароль:")
    password_label_reg.pack()
    password_entry_reg = tk.Entry(registration_window, show="*")
    password_entry_reg.pack()

    confirm_password_label_reg = tk.Label(registration_window, text="Подтвердите пароль:")
    confirm_password_label_reg.pack()
    confirm_password_entry_reg = tk.Entry(registration_window, show="*")
    confirm_password_entry_reg.pack()

    register_button = tk.Button(registration_window, text="Зарегистрировать", command=register_user)
    register_button.pack()

# Основное окно входа
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

login_button = tk.Button(root, text="Вход", command=login)
login_button.pack()

register_button = tk.Button(root, text="Регистрация", command=open_registration_window)
register_button.pack()

root.mainloop()
