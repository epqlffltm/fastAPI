from pydantic import BaseModel
from typing import List

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_completed: bool

    class Config:
        orm_mode = True

class ListToDoResponse(BaseModel):
    todos: List[ToDoSchema]