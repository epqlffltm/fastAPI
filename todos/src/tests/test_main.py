#from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database.connection import get_db
from database.orm import ToDo #테이블 생성을 위해 임포트
#from schema.response import ToDoListSchema

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todos.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ToDo.metadata.create_all(bind=engine)

def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

app.dependency_overrides[get_db] = override_get_db

#client = TestClient(app = app)

def test_health_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_todos(mocker, client):
    #GET 테스트를 하기 전에, 테스트용 DB에 데이터를 미리 3개 넣어둔다.
#    client.post("/todos", json={"contents": "fastapi section 1", "is_done": True})
#    client.post("/todos", json={"contents": "fastapi section 2", "is_done": True})
#    client.post("/todos", json={"contents": "fastapi section 3", "is_done": True})

    # order=ASC
    mocker.patch("main.get_todos", return_value= [
        ToDo(id=1, contents="fastapi section 1", is_done=True),
        ToDo(id=2, contents="fastapi section 2", is_done=False),
    ])
    response = client.get("/todos")
    assert response.status_code == 200
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {"todos": [
        {"id": 1, "contents":"fastapi section 1", "is_done" : True},
        {"id": 2, "contents":"fastapi section 2", "is_done": False},
        #{"id": 3, "contents":"fastapi section 3", "is_done": True},
    ]}

    #order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {"todos": [
        #{"id": 3, "contents":"fastapi section 3", "is_done" : True},
        {"id": 2, "contents":"fastapi section 2", "is_done": False},
        {"id": 1, "contents":"fastapi section 1", "is_done": True},
    ]}
def test_get_todo(client, mocker):
    #200
    mocker.patch("main.get_todo_by_todo_id", return_value = ToDo(id=1, contents="fastapi section 1", is_done=True),)
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "fastapi section 1", "is_done": True}

    #404
    mocker.patch("main.get_todo_by_todo_id", return_value = None)
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not found"}

def test_create_todo(mocker, client):
    create_spy = mocker.spy(ToDo, "create")
    mocker.patch("main.create_todo", return_value=ToDo(id=1, contents="todo", is_done=True))

    body={"contents": "test", "is_done": False,}

    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done == False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}

def test_update_todo(mocker, client):
    #200
    #True와 False를 반복하며 test 할 것
    mocker.patch("main.get_todo_by_todo_id", return_value = ToDo(id=1, contents="fastapi section 1", is_done=True),)
    undone=mocker.patch.object(ToDo, "undone")
    body={"contents": "test", "is_done": False,}
    mocker.patch("main.update_todo", return_value = ToDo(id=1, contents="fastapi section 1", is_done=False),)

    response = client.patch("/todos/1", json={"is_done": False})

    undone.assert_called_once_with()

    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "fastapi section 1", "is_done": False}

    #404
    mocker.patch("main.get_todo_by_todo_id", return_value = None)

    response = client.patch("/todos/1",json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not found"}

def test_delete_todo(mocker, client):
    #204
    mocker.patch("main.get_todo_by_todo_id", return_value = ToDo(id=1, contents="fastapi section 1", is_done=True),)
    mocker.patch("main.delete_todo", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 204

    #404
    mocker.patch("main.get_todo_by_todo_id", return_value = None)
    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not found"}