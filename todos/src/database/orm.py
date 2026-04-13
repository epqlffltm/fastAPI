from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, Integer, String

Base = declarative_base()

class ToDo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"ToDo(id={self.id}, content={self.content}, is_done={self.is_done})"
    