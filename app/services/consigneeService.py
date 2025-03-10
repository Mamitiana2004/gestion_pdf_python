from app.models.test import Consigne
from app.config.database import getSessionLocal

def getAllConsigne():
    session = getSessionLocal()
    consigne = session.query(Consigne).all()
    session.close()
    return consigne

def createNewConsigne(name,adresse):
    session = getSessionLocal()
    newConsigne = Consigne(name = name,adresse = adresse)
    session.add(newConsigne)
    session.commit()
    session.close()

def updateConsigne(id,name,adresse):
    session = getSessionLocal()
    consigne = session.query(Consigne).filter_by(id = id).first()
    
    if consigne is None : 
        return {"error":"error"}

    consigne.name = name
    consigne.adresse = adresse

    session.commit()
    session.close()

def deleteConsigne(id):
    session = getSessionLocal()
    consigne = session.query(Consigne).filter_by(id = id).first()

    session.delete(consigne)
    session.commit()
    session.close()

