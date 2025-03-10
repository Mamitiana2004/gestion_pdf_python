from app.config.database import getSessionLocal
from app.models.test import Contenu


def createNewContenu(pdf_id,page,contenu):
    session = getSessionLocal()
    newContenu = Contenu(pdf_id = pdf_id,page = page,contenu = contenu)
    session.add(newContenu)
    session.commit()
