from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Создание базового класса
Base = declarative_base()


# Определение модели User
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    date_joined = Column(DateTime, default=datetime.utcnow)

    posts = relationship('Post', back_populates='author')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# Определение модели Post
class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    author = relationship('User', back_populates='posts')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# Создание базы данных и таблиц
engine = create_engine('sqlite:///site.db')
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Удаление всех пользователей
session.query(User).delete()
session.commit()

# Добавление пользователей
user1 = User(username='Nikita', email='nikita@examples.com')
user2 = User(username='Paul', email='paul@examples.com')

# Добавляем пользователей в сессию
session.add(user1)
session.add(user2)

# Фиксация изменений
session.commit()

# Удаление всех постов
session.query(Post).delete()
session.commit()

# Добавление постов
post1 = Post(title='Первый пост', content='Содержимое первого поста.', user_id=user1.id)
post2 = Post(title='Второй пост.', content='Содержимое второго поста.', user_id=user2.id)

# Добавляем посты в сессию
session.add(post1)
session.add(post2)

# Фиксация изменений
session.commit()

# Выполнение запросов к базе данных
users = session.query(User).all()
print("Users:")
for user in users:
    print(user)

posts = session.query(Post).all()
print("\nPosts:")
for post in posts:
    print(post)

session.close()
