import jwt
from datetime import datetime,timedelta
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm= ALGORITHM)
    return encode_jwt