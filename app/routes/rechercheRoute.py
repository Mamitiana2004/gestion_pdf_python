from fastapi import APIRouter,Form,Request
from pydantic import BaseModel
from app.services.rechercheService import search_in_contenu

router = APIRouter()


@router.post("/search_in_pdf")
def search_in_pdf(request:Request) :
    text = request._query_params.get("text")
    resultat = search_in_contenu(text)
    return resultat