#main.py
#2026-04-10
#http://127.0.0.1:8000/docs
from database.repository import get_todos
from fastapi import FastAPI, Body, HTTPException ,Depends
from typing import Optional, List
from pydantic import BaseModel
from database.connection import get_db
from database.orm import ToDo
from sqlalchemy.orm import Session


app = FastAPI()

class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

todo_data = {
    1: {"id": 1, "contents": "test1", "is_done": True,},
    2: {"id": 2, "contents": "test2", "is_done": False,},
    3: {"id": 3, "contents": "test3", "is_done": False,},
}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/number")
async def get_number(number: Optional[int] = None):
    return {"ping":"pong","number":number}

@app.get("/todos")
def get_todos_handler(
        order:str | None = None,
        session: Session = Depends(get_db),
        ):
    todos: List[ToDo] = get_todos(session = session)

    #ret = list(todo_data.values())
    if order and order == "DESC":
        return todos[::-1]
    return todos

@app.get("/todos/{id}",status_code=200)
def get_todos_handler(id: int):
    todo = todo_data.get(id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not found")

@app.post("/todos",status_code=201)
def create_todos_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.model_dump()
    return todo_data[request.id]

@app.patch("/todos/{id}",status_code=200)
def get_todos_handler(id: int, is_done: bool = Body(...,embed=True),):
    todo = todo_data.get(id)
    if todo:
        todo["is_done"] = is_done
        return  todo
    raise HTTPException(status_code=404,detail="ToDo Not found")

@app.delete("/todos/{id}", status_code=204)
def delete_todos_handler(id: int):
    todo = todo_data.pop(id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="ToTo Not found")