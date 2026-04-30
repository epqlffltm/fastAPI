#api/user.py
from fastapi import APIRouter, Depends
from schema.response import UserSchema
from database.repository import UserRepository
from schema.request import SignUpRequest
from server.user import UserService

router = APIRouter(prefix="/users")

@router.post("/sign-up",status_code=201,response_model=UserSchema)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    #1. request body(username, password)
    #2. passward -> hashing -> hashed_password
    hashed_password: str = user_service.hash_password(plain_password=request.password)
    #3. user(username, hashed_password)
    from database.orm import User
    user: User = User.create(username=request.username, hashed_password=hashed_password)
    #4. user-> db save
    user: User = user_repo.save_user(user=user)
    #5. return user(id, username)
    user: User = user_repo.save_user(user=user)
    return user
