#database/orm.py
from importlib.resources import contents
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from schema.request import CreateTodoRequest

Base = declarative_base()

class ToDo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"

    @classmethod
    def create(cls, request: CreateTodoRequest, user_id: int) -> "ToDo":
        return cls(contents = request.contents, is_done = request.is_done,user_id=user_id)

    def done(self) -> "ToDo":
        self.is_done = True
        return self

    def undone(self) -> "ToDo":
        self.is_done = False
        return self

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    todos = relationship("ToDo", lazy="joined");

    @classmethod
    def create(cls, username: str, hashed_password: str) -> "User":
        return clsI(username=username, password=hashed_password,)