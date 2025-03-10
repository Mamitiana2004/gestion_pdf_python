from app.models.test import Shipper
from app.config.database import getSessionLocal

def getAllShipper():
    session = getSessionLocal()
    shipper = session.query(Shipper).all()
    session.close()
    return shipper

def createNewShipper(name,adresse):
    session = getSessionLocal()
    new_shipper = Shipper(name = name,adresse = adresse)
    session.add(new_shipper)
    session.commit()
    session.close()

def updateShipper(id,name,adresse):
    session = getSessionLocal()
    shipper = session.query(Shipper).filter_by(id = id).first()
    
    if shipper is None : 
        return {"error":"error"}

    shipper.name = name
    shipper.adresse = adresse

    session.commit()
    session.close()

def deleteShipper(id):
    session = getSessionLocal()
    shipper = session.query(Shipper).filter_by(id = id).first()

    if shipper is None :
        return {"error":"null"}

    session.delete(shipper)
    session.commit()
    session.close()

