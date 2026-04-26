#main.py
#2026-04-10
#http://127.0.0.1:8000/docs
#from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from fastapi import FastAPI, Body, HTTPException ,Depends
from typing import Optional, List
from database.connection import engine # get_db
from database.orm import Base #ToDo
#from sqlalchemy.orm import Session
#from schema.request import CreateTodoRequest
#from schema.response import ToDoListSchema, ToDoSchema
from api import todo

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(todo.router)

"""
todo_data = {
    1: {"id": 1, "contents": "test1", "is_done": True,},
    2: {"id": 2, "contents": "test2", "is_done": False,},
    3: {"id": 3, "contents": "test3", "is_done": False,},
}
"""
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/number")
async def get_number(number: Optional[int] = None):
    return {"ping":"pong","number":number}
"""
@app.get("/todos")
def get_todos_handler(
        order:str | None = None,
        session: Session = Depends(get_db),
        ) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session = session)

    #ret = list(todo_data.values())
    if order and order == "DESC":
        return ToDoListSchema(todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]])
    return ToDoListSchema(todos=[ToDoSchema.model_validate(todo) for todo in todos])

@app.get("/todos/{id}",status_code=200)
def get_todos_handler(id: int, session: Session = Depends(get_db),):
    #todo = todo_data.get(id)
    todo: ToDo | None = get_todo_by_todo_id(session = session, todo_id = id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="ToDo Not found")

@app.post("/todos",status_code=201)
def create_todos_handler(request: CreateTodoRequest, session: Session = Depends(get_db)) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request) #id = none
    todo: ToDo = create_todo(session = session, todo = todo)
    #todo_data[request.id] = request.model_dump()
    #return todo_data[request.id]
    return ToDoSchema.model_validate(todo)

@app.patch("/todos/{id}",status_code=200)
def get_todos_handler(id: int, is_done: bool = Body(...,embed=True),session: Session = Depends(get_db),):
    #todo = todo_data.get(id)
    todo: ToDo | None = get_todo_by_todo_id(session = session, todo_id = id)
    if todo:
        #todo.is_done = is_done
        todo.done() if is_done else todo.undone()
        '''
        if is_done is True:
            todo.done()
        else:
            todo.undone()
        '''
        todo: ToDo = update_todo(session=session, todo=todo)
        #update
        #todo["is_done"] = is_done
        #return  todo
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404,detail="ToDo Not found")

@app.delete("/todos/{id}", status_code=204)
def delete_todos_handler(id: int, session: Session = Depends(get_db)):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=id)
    #todo = todo_data.pop(id, None)
    '''
    if todo:
        # return ToDoSchema.from_orm(todo)
        delete_todo(session = session, todo_id = id)
    raise HTTPException(status_code=404, detail="ToTo Not found")
    '''
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not found")
    delete_todo(session = session, todo_id = id)
"""