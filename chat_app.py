import tkinter as tk
from tkinter import scrolledtext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Message
from datetime import datetime

# Путь к вашей базе данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

class ChatApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Chat App - {self.username}")

        self.message_label = tk.Label(self.root, text="Message:")
        self.message_label.pack()

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack()

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.message_display = scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.message_display.pack()

        self.load_messages()

    def send_message(self):
        message_content = self.message_entry.get().strip()
        if not message_content:
            tk.messagebox.showwarning("Empty Message", "Please enter a message.")
            return

        session = SessionLocal()
        new_message = Message(author=self.username, content=message_content)
        session.add(new_message)
        session.commit()
        session.close()

        self.message_entry.delete(0, tk.END)
        self.load_messages()

    def load_messages(self):
        self.message_display.delete(1.0, tk.END)

        session = SessionLocal()
        messages = session.query(Message).order_by(Message.timestamp.desc()).all()
        session.close()

        for message in messages:
            self.message_display.insert(tk.END, f"[{message.timestamp}] {message.author}: {message.content}\n")
        self.message_display.see(tk.END)

# Пример использования:
def open_chat_app(username):
    chat_root = tk.Tk()
    chat_app = ChatApp(chat_root, username=username)
    chat_root.mainloop()

if __name__ == "__main__":
    open_chat_app("TestUser")
