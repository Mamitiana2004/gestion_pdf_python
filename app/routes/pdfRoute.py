import pdfplumber
from fastapi import UploadFile,File,APIRouter,HTTPException
from app.services.pdfService import process_pdf
import tempfile
import os

router = APIRouter()


@router.post("/extract-plumber")
async def extract_text_pdfplumber(file: UploadFile = File(...)):
    text_data = []
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text = page.extract_text().replace("\n"," ").strip()
            text_data.append(extract_info(text))

    return {"filename": file.filename, "content": text_data}


@router.post("/extract-test")
async def extract(file: UploadFile = File(...)):
     
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(await file.read())
        temp_pdf_path = temp_pdf.name

    try:
        # Extraire le texte du PDF
        
        data = process_pdf(file)
        
        # Supprimer le fichier temporaire
        os.remove(temp_pdf_path)
        
        return data
    except Exception as e:
        # Supprimer le fichier temporaire en cas d'erreur
        os.remove(temp_pdf_path)
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du PDF : {str(e)}")