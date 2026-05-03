#server/user.py
import bcrypt
from datetime import datetime, timedelta
from jose import jwt

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "e21706ab4703cf38deb4a0ffb1270ce89d21459bce9f423e7a81820da443b916"
    jwt_algorithm: str = "HS256"

    def hash_password(self,plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(plain_password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(self.encoding), hashed_password.encode(self.encoding))

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub":username, # unique id
                "exp": datetime.now()+timedelta(hours=24)},
            self.secret_key,
            algorithm=self.jwt_algorithm
        )

    def decode_jwt(self, access_token: str):
        payload = jwt.decode(access_token, self.secret_key, algorithms=[self.jwt_algorithm])
        #expire
        return payload["sub"] #username