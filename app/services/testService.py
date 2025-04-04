import google.generativeai as genai
import pdfplumber
from fastapi import UploadFile, HTTPException
from typing import Dict, List
import json
import re
import os

from app.services.vesselService import createOrGetVessel,getVesselId,searchVesselByName
from app.services.voyageService import getOrCreateVoyage,getVoyageById,getVoyageByVessel,search_voyage_name,search_voyage_entre_date
from app.services.cargoService import createCargo,getCargoByVoyage
from app.services.cargoProduitService import createCargoProduit,getCargo_ProduitByCargo
from app.services.VinProduitService import createVinProduit,getVinByCargo
from app.services.filePDFService import createNewFilePDF,getById
from app.services.pdfService import extract_text_with_plumber
from app.services.contenuService import createNewContenu
from app.services.pdfVoyageService import getPDFVoyagesByPDF_Id,getPDFVoyageByVoyage,createNewPDFVoyages

genai.configure(api_key="AIzaSyDO3i0OLsGj6v_hvVlnJ-MKU1P0-nEH_3Q")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

JSON_TEMPLATE = {
    "vessel": "",               # Code ou nom du navire (ex: "MAERSK HONG KONG")
    "flag": "",                 # Pavillon du navire (ex: "Panama")
    "voyage": "",               # Numéro de voyage (ex: "2107E")    
    "date_of_arrival": "",         # Date d'arrivée (format: "2024-07-15")
    "port_of_loading": "",       # Port de départ (ex: "SHANGHAI") 
    "port_of_discharge": "",       # Date de départ (format: "2024-06-20")
    "cargo": [
        {
            "Booking No(Bn)": "",  
            "shipper": {                # Expéditeur
                "name": "",             # (ex: "COSCO SHIPPING CO., LTD")
                "address": ""           # Adresse complète
            },
            "consignee": {              # Destinataire
                "name": "",             # (ex: "MAERSK BELGIUM NV")
                "address": ""           # Adresse complète
            },
            "notify": {                 # À notifier
                "name": "",             # (ex: "CMA CGM LOGISTICS")
                "address": ""           # Adresse complète
            },
            "quantity":0,  
            "gross_weight": 0.0,      # Poids brut (kg) (ex: 24500.5)
            "measurements": 0.0, 
            "marchandise":"",
            "vin": []          # Numéros VIN si véhicules (ex: ["VF1RFD00654327895"])
        }
    ]
}

def extract_text(file: UploadFile) -> str:
    text_data = []
    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_data.append(text.replace("\n", " "))
        return " ".join(text_data)
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction du PDF: {str(e)}")

import re
import json
from json.decoder import JSONDecodeError

def clean_json_response(text: str) -> dict:
    """
    Nettoie la réponse de Gemini pour obtenir un JSON valide avec gestion d'erreur renforcée
    """
    try:
        # Suppression des marqueurs de code et commentaires
        json_str = re.sub(r'^```(json)?|```$', '', text.strip(), flags=re.MULTILINE)
        json_str = re.sub(r'//.*?\n', '', json_str)  # Supprime les commentaires //
        
        # Correction des problèmes courants
        json_str = json_str.replace("'", '"')  # Remplace les simples quotes
        json_str = re.sub(r'(\w)\s+(\w)', r'\1_\2', json_str)  # Espaces dans les clés
        json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # Virgules traînantes
        
        # Gestion des valeurs non-entre-guillemets
        json_str = re.sub(r':\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([,}])', r': "\1"\2', json_str)
        
        # Validation de base
        json_str = json_str.strip()
        if not json_str.startswith('{'):
            json_str = '{' + json_str
        if not json_str.endswith('}'):
            json_str = json_str + '}'
            
        return json.loads(json_str)
    except JSONDecodeError as e:
        # Log l'erreur et le contexte pour debug
        error_context = text[max(0,e.pos-50):min(len(text),e.pos+50)]
        print(f"ERREUR JSON: {str(e)}")
        print(f"CONTEXTE: ...{error_context}...")
        print(f"TEXTE COMPLET: {text[:1000]}...")  # Truncated pour lisibilité
        raise ValueError(f"La réponse n'est pas un JSON valide: {str(e)}")
    except Exception as e:
        raise ValueError(f"Erreur de traitement JSON: {str(e)}")

def pdf_to_json(file: UploadFile) -> Dict:
    if not file.filename.lower().endswith('.pdf'):
        raise ValueError("Le fichier doit être un PDF")
    
    # Extraction texte
    try:
        text = extract_text(file)
        if not text:
            raise ValueError("Aucun texte trouvé dans le PDF")
    except Exception as e:
        raise ValueError(f"Erreur d'extraction: {str(e)}")
    
    # Prompt
    prompt = f"""
    Transformez ce document maritime en JSON strictement conforme à ce schéma :
    {json.dumps(JSON_TEMPLATE, indent=2, ensure_ascii=False)}

    Règles IMPÉRATIVES:
    - Conservez TOUTES les données originales sans modification
    - Ne pas inventer ou inférer de données manquantes
    - Pour les champs manquants : utiliser null
    - Format des dates : YYYY-MM-DD si disponible
    - Répondez UNIQUEMENT avec le JSON valide, sans commentaires

    Document :
    {text[:500000]}  # Limite raisonnable
    """

    # Appel API avec gestion d'erreur
    try:
        response = model.generate_content(prompt)
        if not response.text:
            raise ValueError("Réponse vide de l'API Gemini")
        
        json_str = clean_json_response(response.text)
        return json_str
    except json.JSONDecodeError as e:
        raise ValueError(f"Réponse JSON invalide: {str(e)}")
    except Exception as e:
        raise ValueError(f"Erreur API Gemini: {str(e)}")
    

async def insert_pdf_data(file:UploadFile):
    file_name = os.path.splitext(file.filename)[0]

    data_file =await file.read()


    try:
        # Extraire le texte du PDF
        
        text_data = extract_text_with_plumber(file)
        pdf_file = createNewFilePDF(nom= file_name,pdf= data_file,page= len(text_data))
        
        for page_number,page_text in text_data:
            createNewContenu(pdf_id= pdf_file.id,page= page_number,contenu= page_text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du PDF : {str(e)}")

    json_data : Dict = pdf_to_json(file)
    if not json_data.get("vessel") or not json_data.get("voyage"):
        raise HTTPException(status_code=400, detail="Données manquantes: vessel ou voyage requis")
    
    vessel = createOrGetVessel(name= json_data["vessel"],flag= json_data["flag"])

    voyage = getOrCreateVoyage(
        code= json_data["voyage"],
        vessel_id= vessel.id,
        date_arrive= json_data["date_of_arrival"]
    )

    createNewPDFVoyages(pdf_id= pdf_file.id, voyage_id= voyage.id)

    for cargo_data in json_data.get("cargo",[]):
        cargo = createCargo(
            voyage_id=voyage.id,
            port_depart=json_data.get("port_of_loading", "Inconnu"),
            shipper=cargo_data.get("shipper", {}).get("name", "Inconnu")+"|"+ cargo_data.get("shipper", {}).get("address"),
            consigne=cargo_data.get("consignee", {}).get("name")+"|"+ cargo_data.get("consignee", {}).get("address"),
            bl_no=cargo_data.get("Booking No(BN)", ""),
            poid=cargo_data.get("gross_weight"),
            volume=cargo_data.get("measurements") 
        )

        if cargo_data.get("marchandise"):
            createCargoProduit(
                produit= cargo_data["marchandise"],
                cargo_id=cargo.id,
                description_produit=f"Shipper: {cargo_data.get('shipper', {}).get('name')}"
            )

        for vin in cargo_data.get("vin", []):
            createVinProduit(
                cargo_id= cargo.id,
                vin = vin
            )

    
    return {"message": "Import réussi", "vessel_id": vessel.id, "voyage_id": voyage.id}

def getDataPDF(pdf_id):
    pdf_voyages = getPDFVoyagesByPDF_Id(pdf_id= pdf_id)
    voyage = getVoyageById(pdf_voyages.voyage_id)
    vessel = getVesselId(voyage.vessel_id)
    cargos = getCargoByVoyage(voyage_id= voyage.id)

    produits = []

    for cargo in cargos:
        cargo_produit = getCargo_ProduitByCargo(cargo.id)
        vin = getVinByCargo(cargo= cargo.id)
        produit = {
            "cargo":cargo,
            "produit":cargo_produit,
            "vin":vin
        }

        produits.append(produit)


    data : Dict = {
        "vessel" : vessel,
        "voyage" : voyage,
        "cargo" : produits,
    }

    return data


def searchPDFByVessel(search):
    vessels = searchVesselByName(search)

    pdfValue :List = []

    for vessel in vessels:
        voyages = getVoyageByVessel(vessel_id= vessel.id)
        for voyage in voyages :
            pdf_voyages = getPDFVoyageByVoyage(voyage_id= voyage.id)
            filePDF = getById(pdf_voyages.pdf_id)
            data ={
                "id": filePDF.id,
                "nom": filePDF.nom,
                "date_ajout":filePDF.date_ajout,
                "nombre_page":filePDF.page
            }
            pdfValue.append(data)

    return pdfValue

def searchPDFByVoyage(search):
    voyages = search_voyage_name(search)

    pdfValue :List = []

    for voyage in voyages :
        pdf_voyages = getPDFVoyageByVoyage(voyage_id= voyage.id)
        filePDF = getById(pdf_voyages.pdf_id)
        
        data ={
                "id": filePDF.id,
                "nom": filePDF.nom,
                "date_ajout":filePDF.date_ajout,
                "nombre_page":filePDF.page
            }
        pdfValue.append(data)
    
    return pdfValue

    

def searchPDFByVoyageDate(date_debut,date_fin):
    voyages = search_voyage_entre_date(date_debut,date_fin)

    pdfValue :List = []

    for voyage in voyages :
        pdf_voyages = getPDFVoyageByVoyage(voyage_id= voyage.id)
        filePDF = getById(pdf_voyages.pdf_id)

        data ={
                "id": filePDF.id,
                "nom": filePDF.nom,
                "date_ajout":filePDF.date_ajout,
                "nombre_page":filePDF.page
            }
        pdfValue.append(data)
    
    return pdfValue

    


    