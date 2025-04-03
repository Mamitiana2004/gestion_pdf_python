from app.services.filePDFService import createNewFilePDF,getAllPdf
from app.services.contenuService import createNewContenu
from fastapi import UploadFile,File,APIRouter,HTTPException
from fastapi.responses import FileResponse
from app.services.pdfService import extract_text_with_plumber,process_pdf
import tempfile
import os
import uuid
from app.services.filePDFService import getPDF
from fastapi.responses import StreamingResponse
import io
from app.services.testService import insert_pdf_data

router = APIRouter()

UPLOAD_DIR = "upload"

# Créer le dossier s'il n'existe pas
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/getAll")
async def getAllPDF():
    resultat = getAllPdf()
    if not resultat:
        raise HTTPException(status_code=404, detail="No files found")

    # Créer une liste pour stocker les informations des fichiers
    files_info = []

    # Parcourir tous les documents
    for document in resultat:
        # Créer un objet BytesIO à partir des données binaires du PDF
        pdf_stream = io.BytesIO(document.pdf)

        # Ajouter les informations du fichier à la liste
        files_info.append({
            "id": document.id,
            "nom": document.nom,
        })
    return {"data":files_info}

@router.post("/import")
async def extract(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF.")
    
    file_name = os.path.splitext(file.filename)[0] 
    file_extension = os.path.splitext(file.filename)[1]  # Récupérer l'extension du fichier
    unique_filename = f"{uuid.uuid4()}{file_extension}"  # Créer un nom de fichier unique

    data_file =await file.read()

    file_pdf =  createNewFilePDF(nom=file_name,nom_serveur=unique_filename,pdf = data_file)


    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(await file.read())
        temp_pdf_path = temp_pdf.name

    try:
        # Extraire le texte du PDF
        
        text_data = extract_text_with_plumber(file)
        
        for page_number,page_text in text_data:
            createNewContenu(pdf_id= file_pdf.id,page= page_number,contenu= page_text)
        


        # Supprimer le fichier temporaire
        os.remove(temp_pdf_path)

        return {"data":text_data}
        
    except Exception as e:
        # Supprimer le fichier temporaire en cas d'erreur
        os.remove(temp_pdf_path)
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du PDF : {str(e)}")
    



@router.get("/download/{name}")
def downloadPdf(name:str):
    file_path = os.path.join(UPLOAD_DIR, name)

    if not os.path.exists(file_path):
        return {"message":"fichier inexistant"}
    
    return FileResponse(
        path=file_path,
        filename="test",
        media_type="application/octet-stream"
    )

@router.get("/{name}")
async def get_pdf(name:str):
    pdf_stream = getPDF(name)
    if pdf_stream:
        return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": f"inline; filename=file.pdf"})
    return {"error": "File not found"}


@router.post("/tt")
async def tet(file: UploadFile):
    return await insert_pdf_data(file)

# @router.post("/import")
# async def upload_pdf(file: UploadFile):
#     if file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Only PDF files are allowed")

#     return StreamingResponse(process_pdf(file), media_type="text/plain")
