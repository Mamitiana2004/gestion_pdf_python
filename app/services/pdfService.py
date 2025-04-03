from transformers import pipeline
import pdfplumber
from fastapi import File, UploadFile
from typing import List, Tuple, Dict


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
        "Shipper_Name": "What is the name of the shipper or SH?",
        "Shipper_Address": "What is the address of the shipper?",
        "Consignee_Name": "What is the name of the consignee or CO?",
        "Consignee_Address": "What is the address of the consignee?",
        "NotifyParty_Name": "What is the name of the notify party or NF?",
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
            print(result)
            data[key] = result["answer"]
        except Exception as e:
            print(e)
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
def process_pdf(file: UploadFile = File(...)) -> List[Dict]:
    # Extraire le texte page par page
    text_data = extract_text_with_plumber(file)

    # Traiter chaque page et extraire les données
    structured_data = []
    for page_text in text_data:
        # createNewContenu(pdf_id= file_pdf.id,page= page_number,contenu= page_text)
        # summary = summarize_text(page_text)
        # print(summary)
        print(page_text)
        page_data = extract_data_with_qa(page_text)
        # insert_data_cargo(data=page_data)
        structured_data.append(page_data)
    return structured_data
 

 
# def insert_data_manifest(data:Dict):
#     vessel_data : Dict = data.get("Vessel",{})
#     vessel_code = vessel_data.get("Code")
#     vessel = vessel_data.get("Name")
#     if vessel_code not in vessel :
#         vessel = vessel_code+" "+vessel

#     flag = vessel_data.get("Flag")
#     voyage = vessel_data.get("Voyage")
#     date_arrive = vessel_data.get("DateOfArrival")
#     manifest = importManifest(
#         vessel= vessel,
#         flag= flag,
#         voyage= voyage,
#         date_arrive= date_arrive
#     )
#     return manifest

# def insert_data_shipper(data:Dict):
#     shipper_data : Dict = data.get("Shipper",{})
#     name = shipper_data.get("Name")
#     adresse = shipper_data.get("Adresse")
#     shipper = importShipper(name=name,adresse=adresse)
#     return shipper

# def insert_data_consigne(data:Dict):
#     consigne_data : Dict = data.get("Consignee",{})
#     name = consigne_data.get("Name")
#     adresse = consigne_data.get("Adresse")
#     return importConsigne(name=name,adresse=adresse)

# def insert_data_cargo(data:Dict):
#     manifest = insert_data_manifest(data)
#     shipper = insert_data_shipper(data)
#     consigne = insert_data_consigne(data)

#     description = data.get("DescriptionOfGoods")
#     weight : str = data.get("Weight")
#     if not weight.isnumeric():
#         weight = 0
    
#     mesurement :str = data.get("Measurement")
#     if not mesurement.isnumeric():
#         mesurement = 0
#     bl_value = data.get("B/LNo")

#     cargo = importCargo(
#         bl_no= bl_value,
#         manifest_id= manifest.id,
#         shipper_id = shipper.id,
#         consigne_id =consigne.id,
#         description=description,
#         weight=weight,
#         mesurement=mesurement
#     )
#     return cargo
    

# def summarize_text(text, max_length=130, min_length=30):
#     summarizer = pipeline("summarization")
#     summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
#     return summary[0]['summary_text']

