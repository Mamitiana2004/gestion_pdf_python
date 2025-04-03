from fastapi import APIRouter,Form,Request
from app.services.rechercheService import search_in_contenu,search_pdf_name

router = APIRouter()


@router.get("/search_in_pdf")
def search_in_pdf(request:Request) :
    text = request._query_params.get("text")
    resultat = search_in_contenu(text)
    return resultat

@router.get("/search_pdf_name")
def search_pdf(request : Request):
    text = request._query_params.get("text")
    resultat = search_pdf_name(text)
    return {"resultat":resultat}