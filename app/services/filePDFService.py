from app.config.database import getSessionLocal
from app.models.model import FilePDF
import io

def getAllPdf():
    session = getSessionLocal()
    filePdf =  session.query(FilePDF).all()
    session.close()
    return filePdf

def createNewFilePDF(nom,nom_serveur,pdf):
    session = getSessionLocal()
    newFilePDF = FilePDF(nom = nom,nom_serveur = nom_serveur,pdf = pdf)
    session.add(newFilePDF)
    session.commit()
    session.refresh(newFilePDF)
    return newFilePDF

def getById(id):
    session = getSessionLocal()
    filePDF = session.query(FilePDF).filter_by(id = id).first()
    session.close()
    return filePDF

def getPDF(nom_serveur):
    session = getSessionLocal()
    filePDF = session.query(FilePDF).filter_by(nom_serveur = nom_serveur).first()
    file_stream = io.BytesIO(filePDF.pdf)
    session.close()
    return file_stream