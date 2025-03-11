from transformers import pipeline
import pdfplumber
from fastapi import File, UploadFile
from typing import List, Dict,Tuple
from app.services.contenuService import createNewContenu
from app.services.manifestService import importManifest

# Fonction pour extraire le texte d'un PDF page par page
def extract_text_with_plumber(file: UploadFile = File(...)) -> List[Tuple[int, str]]:
    text_data = []
    i = 0
    with pdfplumber.open(file.file) as pdf:
        for page_number,page in enumerate(pdf.pages,start=1):
            text = page.extract_text()
            i = i+1
            if i == 2 :
                if text:
                    text_data.append((page_number,text.replace("\n", " ")))
            if i == 3:
                break
    return text_data


# Fonction pour extraire les informations structurées avec un modèle de question-réponse
def extract_data_with_qa(text: str) -> Dict:
    # Charger un modèle de question-réponse
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

    # Questions pour extraire les champs
    questions = {
        "Vessel_Code": "What is the vessel code?",
        "Vessel_Name": "What is the name of the vessel?",
        "Voyage": "What is the voyage code?",
        "Flag": "What is the flag of the vessel?",
        "DateOfSail": "What is the date of sail?",
        "DateOfArrival": "What is the date of arrival?",
        "PortOfLoading": "What is the port of loading?",
        "PortOfDischarge": "What is the port of discharge?",
        "PlaceOfDelivery": "What is the place of delivery?",
        "BLNo": "What is the B/L number?",
        "BookingNo": "What is the booking number?",
        "Shipper_Name": "What is the name of the shipper?",
        "Shipper_Address": "What is the address of the shipper?",
        "Consignee_Name": "What is the name of the consignee?",
        "Consignee_Address": "What is the address of the consignee?",
        "NotifyParty_Name": "What is the name of the notify party?",
        "NotifyParty_Address": "What is the address of the notify party?",
        "MarksAndNos": "What are the marks and numbers?",
        "DescriptionOfGoods": "What is the description of goods?",
        "Weight": "What is the weight of the goods?",
        "Measurement": "What is the measurement of the goods?",
        "FreightDetails": "What are the freight details?",
    }

    # Extraire les réponses
    data = {}
    for key, question in questions.items():
        try:
            result = qa_pipeline(question=question, context=text)
            data[key] = result["answer"]
        except Exception as e:
            data[key] = "Non trouvé"  # En cas d'erreur, retourner "Non trouvé"

    # Structurer les données dans le format JSON souhaité
    structured_data = {
        "Vessel": {
            "Code": data.get("Vessel_Code"),
            "Name": data.get("Vessel_Name"),
            "Voyage": data.get("Voyage"),
            "Flag": data.get("Flag"),
            "DateOfSail": data.get("DateOfSail"),
            "DateOfArrival": data.get("DateOfArrival"),
            "PortOfLoading": data.get("PortOfLoading"),
            "PortOfDischarge": data.get("PortOfDischarge"),
            "PlaceOfDelivery": data.get("PlaceOfDelivery"),
        },
        "B/LNo": data.get("BLNo"),
        "BookingNo": data.get("BookingNo"),
        "Shipper": {
            "Name": data.get("Shipper_Name"),
            "Address": data.get("Shipper_Address"),
        },
        "Consignee": {
            "Name": data.get("Consignee_Name"),
            "Address": data.get("Consignee_Address"),
        },
        "NotifyParty": {
            "Name": data.get("NotifyParty_Name"),
            "Address": data.get("NotifyParty_Address"),
        },
        "MarksAndNos": data.get("MarksAndNos"),
        "DescriptionOfGoods": data.get("DescriptionOfGoods"),
        "Weight": data.get("Weight"),
        "Measurement": data.get("Measurement"),
        "FreightDetails": data.get("FreightDetails"),
    }

    return structured_data

# Fonction principale pour traiter le PDF et retourner un tableau de JSON
def process_pdf(file: UploadFile = File(...),file_pdf = None) -> List[Dict]:
    # Extraire le texte page par page
    text_data = extract_text_with_plumber(file)

    # Traiter chaque page et extraire les données
    structured_data = []
    for page_number,page_text in text_data:
        createNewContenu(pdf_id= file_pdf.id,page= page_number,contenu= page_text)
        page_data = extract_data_with_qa(page_text)
        structured_data.append(page_data)
        insert_data_manifest(page_data)
    return structured_data
 
def insert_data_manifest(data:Dict):
    vessel_data : Dict = data.get("Vessel",{})
    vessel_code = vessel_data.get("Code")
    vessel = vessel_data.get("Name")
    if vessel_code not in vessel :
        vessel = vessel_code+" "+vessel

    flag = vessel_data.get("Flag")
    voyage = vessel_data.get("Voyage")
    date_arrive = vessel_data.get("DateOfArrival")
    importManifest(
        vessel= vessel,
        flag= flag,
        voyage= voyage,
        date_arrive= date_arrive
    )









