from pydantic import BaseModel#, ConfigDict
#from schema.response import ToDoSchema


class CreateTodoRequest(BaseModel):
    #id: int
    contents: str
    is_done: bool

#    model_config= ConfigDict(from_attributes=True)

#class ToDoListSchema(BaseModel):
#    todos: list[ToDoSchema]

class SignUpRequest(BaseModel):
    username: str
    password: str

