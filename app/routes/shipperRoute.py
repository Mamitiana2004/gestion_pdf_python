from app.services.shipperService import getAllShipper,createNewShipper,updateShipper,deleteShipper
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter()



@router.get("/getAll")
def getAllUser() : 
    utilisateurs = getAllShipper()
    return utilisateurs

class AddShipper(BaseModel):
    name:str
    adresse:str

class AllShipper(BaseModel):
    id:int
    name:str
    adresse:str

@router.post("/create")
def create_shipper(request:AddShipper):
    createNewShipper(name=request.name,adresse=request.adresse)
    return {"success":"success"}


@router.put("/update")
def update_shipper(request:AllShipper):
    updateShipper(id=request.id,name=request.name,adresse=request.adresse)
    return {"success":"true"}

@router.delete("/delete/{id}")
def delete_shipper(id:int):
    deleteShipper(id)
    return {"success":"true"}