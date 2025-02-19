import pdfplumber
from fastapi import UploadFile,File,APIRouter


router = APIRouter()


@router.post("/extract-plumber")
async def extract_text_pdfplumber(file: UploadFile = File(...)):
    text_data = []
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text = page.extract_text().replace("\n"," ").strip()
            text_data.append(text)

    return {"filename": file.filename, "content": text_data}