from app.models.test import Consigne
from app.config.database import getSessionLocal
from app.services.rechercheService import sont_presque_pareils

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
    session.refresh(newConsigne)
    session.close()
    return newConsigne

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

def getConsigneByName(name):
    session = getSessionLocal()
    consigne = session.query(Consigne).filter_by(name = name).first()
    session.close()
    return consigne

def importConsigne(name,adresse):
    session = getSessionLocal()
    consigneExistant = getConsigneByName(name=name)
    if consigneExistant :
        session.close()
        return consigneExistant
    
    consignes = session.query(Consigne).all()
    session.close()
    for consigne in consignes :
        isPareil = sont_presque_pareils(consigne.name,name)
        if isPareil :
            return consigne
        
    newConsigne = createNewConsigne(name,adresse)
    return newConsigne