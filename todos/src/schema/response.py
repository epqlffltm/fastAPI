from pydantic import BaseModel, ConfigDict
from typing import List

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    #class Config:
    model_config = ConfigDict(from_attributes=True)

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]