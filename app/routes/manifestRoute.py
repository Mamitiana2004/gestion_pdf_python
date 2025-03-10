from fastapi import APIRouter
from pydantic import BaseModel
from app.services.manifestService import getAllManifest,createNewManifest
from datetime import datetime

router = APIRouter()

@router.get("/getAll")
def getAll():
    result = getAllManifest()
    return result

class AddManifest(BaseModel):
    vessel:str
    flag:str
    voyage:str
    dateArrive:str

@router.post("/create")
def create_manifest(request:AddManifest):
    dateArrive = datetime.strptime(request.dateArrive,"%Y-%m-%d")
    createNewManifest(vessel=request.vessel,flag=request.flag,date_arrive= dateArrive,voyage= request.voyage)
    return {"success":"success"}