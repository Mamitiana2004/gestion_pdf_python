from app.models.test import Manifest
from app.config.database import getSessionLocal
from app.services.rechercheService import sont_presque_pareils

def getAllManifest():
    session = getSessionLocal()
    manifests = session.query(Manifest).all()
    session.close()
    return manifests

def getManifestById(id):
    session = getSessionLocal()
    manifest = session.query(Manifest).filter_by(id=id).first()
    session.close()
    return manifest


def createNewManifest(vessel,flag,voyage,date_arrive):
    session = getSessionLocal()
    newManifest = Manifest(vessel = vessel,flag = flag,voyage = voyage,date_arrive = date_arrive)
    session.add(newManifest)
    session.commit()
    session.refresh(newManifest)
    session.close()
    return newManifest

def updateManifest(id,vessel,flag,voayge,date_arrive):
    session = getSessionLocal()
    manifest = getManifestById(id)
    if manifest is None :
        return {"error":"eror"}
    
    manifest.vessel = vessel
    manifest.voyage = voayge
    manifest.flag = flag
    manifest.date_arrive = date_arrive

    session.commit()
    session.close()



def deleteManifest(id):
    session = getSessionLocal()
    manifest = getManifestById(id)
    session.delete(manifest)
    session.commit()
    session.close()

def getManifestByVessel(vessel):
    session = getSessionLocal()
    manifest = session.query(Manifest).filter_by(vessel = vessel).first()
    session.close()
    return manifest


def importManifest(vessel,flag,voyage,date_arrive):
    session = getSessionLocal()
    manifestExistant = getManifestByVessel(vessel= vessel)
    if manifestExistant:
        session.close()
        return manifestExistant

    manifests = session.query(Manifest).all()
    for manifest in manifests : 
        isPareil = sont_presque_pareils(manifest.vessel,vessel)
        if isPareil :
            session.close()
            return manifest

    session.close()
    newManifest = createNewManifest(
        vessel= vessel,
        voyage= voyage,
        flag= flag,
        date_arrive=date_arrive
    )   
    return newManifest