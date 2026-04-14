from sqlalchemy import select
from sqlalchemy.orm import Session
from database.orm import ToDo
from typing import List

def get_todos(session: Session) -> List:
    return list(session.scalars(select(ToDo)))

def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))