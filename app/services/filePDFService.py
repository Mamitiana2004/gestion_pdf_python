from app.config.database import getSessionLocal
from app.models.test import FilePDF

def createNewFilePDF(nom,nom_serveur):
    session = getSessionLocal()
    newFilePDF = FilePDF(nom = nom,nom_serveur = nom_serveur)
    session.add(newFilePDF)
    session.commit()
    session.refresh(newFilePDF)
    return newFilePDF

def getById(id):
    session = getSessionLocal()
    filePDF = session.query(FilePDF).filter_by(id = id).first()
    session.close()
    return filePDF