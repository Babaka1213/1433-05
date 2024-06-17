from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Создание подключения к SQLite базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель пользователя для ORM
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

# Создание таблицы в базе данных
Base.metadata.create_all(bind=engine)

def create_user(username: str, password_hash: str):
    db = SessionLocal()
    user = User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(username: str):
    db = SessionLocal()
    return db.query(User).filter(User.username == username).first()

def update_user_password(username: str, new_password_hash: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.password_hash = new_password_hash
        db.commit()
        db.refresh(user)
        return True
    return False
