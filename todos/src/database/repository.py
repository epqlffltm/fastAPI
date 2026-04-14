from sqlalchemy import select
from sqlalchemy.orm import Session
from database.orm import ToDo
from typing import List

def get_todos(session: Session) -> List:
    return list(session.scalars(select(ToDo)))