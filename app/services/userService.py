import jwt
from app.config.database import getConnection
from app.services.tokenService import create_access_token
from app.config.config import ALGORITHM,SECRET_KEY


def login(identifiant,password):
    conn = getConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id,password FROM utilisateur WHERE identifiant=%s",(identifiant,))
        user = cursor.fetchone()

        if user is None:
            return {"error":"Utilisateur inconnue"}
        
        id,stored_hash = user
        if password == stored_hash :
            return {"token":create_access_token({"user_id":id,"identifiant":identifiant}),"user":{"user_id":id,"identifiant":identifiant}}
        else :
            return {"error":"Mot de passe incorrect"}
    finally:
        cursor.close()
        conn.close()

def verifyToken(token) :
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return 0
    except jwt.InvalidTokenError:
        return 1
