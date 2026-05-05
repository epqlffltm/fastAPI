#api/user.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from cache import redis_client
from schema.response import UserSchema, JWTResponse
from database.repository import UserRepository
from schema.request import SignUpRequest, LoginRequest, CreateOTPRequest, VerifyOTPRequest
from security import get_access_token
from server.user import UserService
from database.orm import User

router = APIRouter(prefix="/users")

@router.post("/sign-up",status_code=201,response_model=UserSchema)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    #1. request body(username, password)
    #2. password -> hashing -> hashed_password
    hashed_password: str = user_service.hash_password(plain_password=request.password)
    #3. user(username, hashed_password)
    user: User = User.create(username=request.username, hashed_password=hashed_password)
    #4. user-> db save
    user: User = user_repo.save_user(user=user)
    #5. return user(id, username)
    #user: User = user_repo.save_user(user=user)
    return user

@router.post("/log-in")
def user_log_in_handler(request: LoginRequest,
                        user_service: UserService = Depends(),
                        user_repo: UserRepository = Depends(),):
    #1. request body(username, password)
    #2. db read user
    user: User | None = user_repo.get_user_by_username(username=request.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #3. user.password, request.password -> bcrypt.checkpw
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    )
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")
    #4. create jwt
    access_token: str = user_service.create_jwt(username = user.username)
    #5. return jwt
    return JWTResponse(access_token=access_token)

#회원가입 가능/로그인
#이메일 알람: 회원가입->이메일 인증(otp) -> 유저 이메일 저장 -> 이메일 알림
#POST/user/email/otp -> key:email, value: otp exp: 3min
#POST/users/email/otp/verify -> request(email, otp) -> user(email)

@router.post("/email/otp")
def create_otp_handler(
        request: CreateOTPRequest,
        _: str = Depends(get_access_token),
        user_service: UserService = Depends(),
):
    # 1. access_token
    # 2. request body(email)
    # 3. otp create(random 4 digit)
    otp: int = user_service.create_otp()
    # 4. redis otp(email:otp exp=3mit)
    redis_client.set(request.email, otp, ex=180)
    #redis_client.expire(request.email, 3*60)
    # 5. send otp tp email
    return{"otp":otp}

@router.post("/email/otp/verify/")
def verify_otp_handler(
        request: VerifyOTPRequest,
        background_tasks: BackgroundTasks,
        access_token: str = Depends(get_access_token),
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    # 1. access_token
    # 2. request body(email, otp)
    # 3. request.otp == redis.get(email)
    otp: str | None = redis_client.get(request.email)
    if not otp:
        raise HTTPException(status_code=404, detail="bad request")

    if request.otp != int(otp):
        raise HTTPException(status_code=404, detail="bad request")

    # 4. user(email)
    username: str = user_service.decode_jwt(access_token)
    user: User | None = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #save email to user

    #send email to user
    background_tasks.add_task(
        user_service.send_email_to_user,
        mail="admin@fastapi.com"
    )
    #user_service.send_email_to_user(email="admin@fastapi.com")
    return UserSchema.model_validate(user)
