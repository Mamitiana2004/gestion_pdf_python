from app.services.filePDFService import createNewFilePDF
from fastapi import UploadFile,File,APIRouter,HTTPException
from app.services.pdfService import process_pdf,extract_text_with_plumber
from app.services.contenuService import createNewContenu
import tempfile
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "upload"

# Créer le dossier s'il n'existe pas
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/extract-test")
async def extract(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF.")
    
    file_name = os.path.splitext(file.filename)[0] 
    file_extension = os.path.splitext(file.filename)[1]  # Récupérer l'extension du fichier
    unique_filename = f"{uuid.uuid4()}{file_extension}"  # Créer un nom de fichier unique

    # Chemin complet du fichier sur le serveur
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    file_pdf =  createNewFilePDF(nom=file_name,nom_serveur=unique_filename)

    text_data = extract_text_with_plumber(file)
    for page_number,page_text in text_data:
        createNewContenu(file_pdf.id,page_number,page_text) 

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
    #     temp_pdf.write(await file.read())
    #     temp_pdf_path = temp_pdf.name

    # try:
    #     # Extraire le texte du PDF
        
    #     data = process_pdf(file)
        
    #     # Supprimer le fichier temporaire
    #     os.remove(temp_pdf_path)
        
    #     return data
    # except Exception as e:
    #     # Supprimer le fichier temporaire en cas d'erreur
    #     os.remove(temp_pdf_path)
    #     raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du PDF : {str(e)}")