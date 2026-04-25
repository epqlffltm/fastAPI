from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"
#SQLite 파일 경로 (현재 폴더에 todos.db로 생성됨)
DATABASE_URL = "sqlite:///todos.db"

#SQLite 전용 옵션 추가 (FastAPI의 멀티스레드 환경을 위해 필수)
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()