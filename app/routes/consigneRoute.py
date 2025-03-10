from fastapi import APIRouter
from app.services.consigneeService import getAllConsigne

router = APIRouter()

@router.get("/getAll")
def getAll():
    result = getAllConsigne()
    return result