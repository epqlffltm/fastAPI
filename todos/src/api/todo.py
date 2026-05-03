#api/dodo.py
#2026-04-10
#http://127.0.0.1:8000/docs
from database.repository import ToDoRepository, UserRepository  # get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from typing import Optional, List
from database.connection import get_db
from database.orm import ToDo, User
from sqlalchemy.orm import Session
from schema.request import CreateTodoRequest
from schema.response import ToDoListSchema, ToDoSchema
from security import get_access_token
from server.user import UserService

router = APIRouter(prefix="/todos")

"""
todo_data = {
    1: {"id": 1, "contents": "test1", "is_done": True,},
    2: {"id": 2, "contents": "test2", "is_done": False,},
    3: {"id": 3, "contents": "test3", "is_done": False,},
}
"""


@router.get("")
def get_todos_handler(
        access_token:str = Depends(get_access_token),
        order: str | None = None,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
        #session: Session = Depends(get_db),
        todo_repo: ToDoRepository = Depends(),
) -> ToDoListSchema:

    username: str = user_service.decode_jwt(access_token=access_token)
    user: User | None = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")


    print(access_token)
    todos: List[ToDo] = user.todos

    # ret = list(todo_data.values())
    if order and order == "DESC":
        return ToDoListSchema(todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]])
    return ToDoListSchema(todos=[ToDoSchema.model_validate(todo) for todo in todos])


@router.get("/{id}", status_code=200)
def get_todo_handler(id: int, todo_repo: ToDoRepository = Depends(),):
    # todo = todo_data.get(id)
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="ToDo Not found")


@router.post("", status_code=201)
def create_todo_handler(request: CreateTodoRequest, todo_repo: ToDoRepository = Depends(),) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request)  # id = none
    todo: ToDo = todo_repo.create_todo(todo=todo)
    # todo_data[request.id] = request.model_dump()
    # return todo_data[request.id]
    return ToDoSchema.model_validate(todo)


@router.patch("/{id}", status_code=200)
def update_todo_handler(id: int, is_done: bool = Body(..., embed=True), todo_repo: ToDoRepository = Depends(),):
    # todo = todo_data.get(id)
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=id)
    if todo:
        # todo.is_done = is_done
        todo.done() if is_done else todo.undone()
        '''
        if is_done is True:
            todo.done()
        else:
            todo.undone()
        '''
        todo: ToDo = todo_repo.update_todo(todo=todo)
        # update
        # todo["is_done"] = is_done
        # return  todo
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="ToDo Not found")


@router.delete("/{id}", status_code=204)
def delete_todo_handler(id: int, todo_repo: ToDoRepository = Depends()):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=id)
    # todo = todo_data.pop(id, None)
    '''
    if todo:
        # return ToDoSchema.from_orm(todo)
        delete_todo(session = session, todo_id = id)
    raise HTTPException(status_code=404, detail="ToTo Not found")
    '''
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not found")
    todo_repo.delete_todo(todo_id=id)