import jwt
from app.config.database import getSessionLocal
from app.services.tokenService import create_access_token
from app.config.config import ALGORITHM,SECRET_KEY
from app.models.test import Utilisateur


def login(identifiant,password):    
    session = getSessionLocal()


    utilisateur = session.query(Utilisateur).filter_by(identifiant=identifiant).first()
    
    if utilisateur is None:
        return {"error":"Utilisateur inconnue"}
     
    if  utilisateur.password == password :
        return {"token":create_access_token({"user_id":utilisateur.id,"identifiant":utilisateur.identifiant}),"user":{"user_id":utilisateur.id,"identifiant":utilisateur.identifiant}}
    else :
        return {"error":"Mot de passe incorrect"}
    

def verifyToken(token) :
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return 0
    except jwt.InvalidTokenError:
        return 1
    
def getAll():
    session = getSessionLocal()
    utilisateurs = session.query(Utilisateur).all()
    return {"data":utilisateurs}

def createNewUser(identifiant,password):
    session = getSessionLocal()
    newUtilisateur = Utilisateur(identifiant=identifiant,password=password)
    session.add(newUtilisateur)
    session.commit()
    print(newUtilisateur.identifiant)
    session.close()

def updateUser(id,identifiant,password):
    session = getSessionLocal()
    utilisateur = session.query(Utilisateur).filter_by(id = id).first()

    if utilisateur is None :
        return {"error":"null"}
    
    utilisateur.identifiant = identifiant
    utilisateur.password = password

    session.commit()
    session.close()

    return {"success":"true"}

def deleteUser(id) : 
    session = getSessionLocal()
    utilisateur = session.query(Utilisateur).filter_by(id = id).first()

    if utilisateur is None :
        return {"error":"null"}
    
    session.delete(utilisateur)
    session.commit()
    session.close()

