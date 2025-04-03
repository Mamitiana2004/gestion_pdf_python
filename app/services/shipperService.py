from app.models.test import Shipper
from app.config.database import getSessionLocal
from app.services.rechercheService import sont_presque_pareils

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
    session.refresh(new_shipper)
    session.close()
    return new_shipper

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

def getShipperByName(name):
    session = getSessionLocal()
    shipper = session.query(Shipper).filter_by(name = name).first()
    session.close()
    return shipper

def importShipper(name,adresse):
    session = getSessionLocal()
    shipperExistant = getShipperByName(name)
    if shipperExistant : 
        session.close()
        return shipperExistant
    
    shippers = session.query(Shipper).all()
    session.close()

    for shipper in shippers :
        isPareil = sont_presque_pareils(shipper.name,name)
        if isPareil : 
            return shipper
        
    newShipper = createNewShipper(name=name,adresse=adresse)
    return newShipper