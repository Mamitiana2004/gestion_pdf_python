from fastapi import APIRouter
from app.services.consigneeService import getAllConsigne,createNewConsigne,updateConsigne,deleteConsigne
from pydantic import BaseModel

router = APIRouter()

@router.get("/getAll")
def getAll():
    result = getAllConsigne()
    return result


class AddConsigne(BaseModel):
    name:str
    adresse:str

@router.post("create")
def create_new_consigne(request:AddConsigne):
    createNewConsigne(name=request.name,adresse=request.adresse)
    return {"success":"TRUE"}

class AllConsigne(BaseModel):
    id:int
    name:str
    adresse:str

@router.put("/update")
def update_consigne(request:AllConsigne):
    updateConsigne(id=request.id,name=request.name,adresse=request.adresse)
    return {"success":"TRUE"}

@router.delete("/delete/{id}")
def delete_consigne(id:int):
    deleteConsigne(id)
    return {"success":"TRUE"}