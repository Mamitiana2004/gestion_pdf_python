from app.models.model import CargoProduit
from app.config.database import getSessionLocal

def createCargoProduit(produit , cargo_id, description_produit): 
    session = getSessionLocal()

    newCargoProduit = CargoProduit(
        produit = produit,
        cargo_id = cargo_id,
        description_produit = description_produit
    )

    session.add(newCargoProduit)

    session.commit()
    session.refresh(newCargoProduit)
    session.close()

    return newCargoProduit


def getCargo_ProduitByCargo(cargo_id):
    session = getSessionLocal()
    cargo_produit = session.query(CargoProduit).filter_by(cargo_id = cargo_id).all()
    session.close()
    return cargo_produit