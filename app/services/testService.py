import google.generativeai as genai
import pdfplumber
from fastapi import UploadFile, File,HTTPException
from typing import Dict, List
import json
import re


from app.services.vesselService import createOrGetVessel
from app.services.voyageService import getOrCreateVoyage
from app.services.cargoService import createCargo
from app.services.cargoProduitService import createCargoProduit

genai.configure(api_key="AIzaSyDO3i0OLsGj6v_hvVlnJ-MKU1P0-nEH_3Q")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

JSON_TEMPLATE = {
    "vessel": "",               # Code ou nom du navire (ex: "MAERSK HONG KONG")
    "flag": "",                 # Pavillon du navire (ex: "Panama")
    "voyage": "",               # Numéro de voyage (ex: "2107E")
    "date_of_sail": "",         # Port d'arrivée (ex: "ANTWERP")
    "date_of_arrival": "",         # Date d'arrivée (format: "2024-07-15")
    "port_of_loading": "",       # Port de départ (ex: "SHANGHAI") 
    "port_of_discharge": "",       # Date de départ (format: "2024-06-20")
    "cargo": [
        {
            "B/L No": "",  
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

def extract_text_with_plumber(file: UploadFile) -> str:
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

def clean_json_response(text: str) -> str:
    """
    Nettoie la réponse de Gemini pour obtenir un JSON valide
    """
    try:
        # Suppression des marqueurs de code
        json_str = text.strip()
        json_str = re.sub(r'^```json|```$', '', json_str, flags=re.MULTILINE)
        
        # Correction des problèmes courants
        json_str = json_str.replace("'", '"')  # Remplace les simples quotes
        json_str = re.sub(r'(\w)\s+(\w)', r'\1_\2', json_str)  # Espaces dans les clés
        json_str = re.sub(r',\s*}', '}', json_str)  # Virgules traînantes
        json_str = re.sub(r',\s*]', ']', json_str)  # Virgules traînantes
        
        # Validation de base
        if not json_str.strip().startswith('{'):
            json_str = '{' + json_str
        if not json_str.strip().endswith('}'):
            json_str = json_str + '}'
            
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        error_context = json_str[max(0,e.pos-50):min(len(json_str),e.pos+50)]
        raise ValueError(f"Invalid JSON at position {e.pos}: ...{error_context}...")
    except Exception as e:
        raise ValueError(f"Cleaning failed: {str(e)}")

def pdf_to_json(file: UploadFile) -> Dict:
    if not file.filename.lower().endswith('.pdf'):
        raise ValueError("Le fichier doit être un PDF")
    
    # Extraction texte
    try:
        text = extract_text_with_plumber(file)
        if not text:
            raise ValueError("Aucun texte trouvé dans le PDF")
    except Exception as e:
        raise ValueError(f"Erreur d'extraction: {str(e)}")
    
    # Prompt
    prompt = f"""
    Transformez ce document maritime en JSON strictement conforme à ce schéma :
    {json.dumps(JSON_TEMPLATE, indent=2, ensure_ascii=False)}

    Règles :
    - Conservez TOUTES les données originales sans modification
    - Ne pas inventer ou inférer de données manquantes
    - Pour les champs manquants : utiliser null
    - Format des dates : YYYY-MM-DD si disponible
    - Répondez UNIQUEMENT avec le JSON valide, sans commentaires

    Document :
    {text[:100000]}  # Limite raisonnable
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
    

def insert_pdf_data(file):
    json_data : Dict = pdf_to_json(file)
    if not json_data.get("vessel") or not json_data.get("voyage"):
        raise HTTPException(status_code=400, detail="Données manquantes: vessel ou voyage requis")
    
    vessel = createOrGetVessel(name= json_data["vessel"],flag= json_data["flag"])

    voyage = getOrCreateVoyage(
        code= json_data["voyage"],
        vessel_id= vessel.id,
        date_arrive= json_data["date_of_arrival"]
    )

    for cargo_data in json_data("cargo",[]):
        cargo = createCargo(
            voyage_id=voyage.id,
            port_depart=json_data.get("port_of_loading", "Inconnu"),
            date_depart=json_data["date_of_sail"],
            shipper=cargo_data.get("shipper", {}).get("name", "Inconnu")+" "+ cargo_data.get("shipper", {}).get("address"),
            consigne=cargo_data.get("consignee", {}).get("name")+" "+ cargo_data.get("consignee", {}).get("address"),
            bl_no=cargo_data.get("B/L No", ""),
            poid=cargo_data.get("gross_weight"),
            volume=cargo_data.get("measurements") 
        )

        if cargo_data.get("marchandise"):
            produit = createCargoProduit(
                produit= cargo_data["marchandise"],
                cargo_id=cargo.id,
                description_produit=f"Shipper: {cargo_data.get('shipper', {}).get('name')}"
            )