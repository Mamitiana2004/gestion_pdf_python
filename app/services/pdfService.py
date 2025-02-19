import re
import pdfplumber
from fastapi import File,UploadFile


def extract_text_with_plumber(file: UploadFile = File(...)):
    text_data=[]
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            text_data.append(text.replace("\n"," "))
        
    return text_data




def extract_info(pdf_text):
    data = {}
    # Numéro de suivi (ex: "Tracking Number: AB123456789")
    tracking_pattern = r"VESSEL\s:\s*(\w+)"
    match = re.search(tracking_pattern, pdf_text)
    data["vessel"] = match.group(1) if match else "Non trouvé"

    # Expéditeur (ex: "Shipper: John Doe, New York, USA")
    shipper_pattern = r"Voyage:\s*([\w\s,]+)"
    match = re.search(shipper_pattern, pdf_text)
    data["shipper"] = match.group(1) if match else "Non trouvé"

    # Destinataire (ex: "Consignee: Jane Smith, Paris, France")
    consignee_pattern = r"Flag:\s*([\w\s,]+)"
    match = re.search(consignee_pattern, pdf_text)
    data["consignee"] = match.group(1) if match else "Non trouvé"

    # Date d'expédition (ex: "Date: 12/02/2024")
    date_pattern = r"Date \s*(\d{2}/\d{2}/\d{4})"
    match = re.search(date_pattern, pdf_text)
    data["date"] = match.group(1) if match else "Non trouvé"