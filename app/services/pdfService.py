import pdfplumber
from fastapi import File, UploadFile
from typing import List, Tuple


# Fonction pour extraire le texte d'un PDF page par page
def extract_text_with_plumber(file: UploadFile = File(...)) -> List[Tuple[int, str]]:
    text_data = []
    with pdfplumber.open(file.file) as pdf:
        for page_number,page in enumerate(pdf.pages,start=1):
            text = page.extract_text()
            if text:
                text_data.append((page_number,text.replace("\n", " ")))
            break        
    return text_data

