from app.config.database import getSessionLocal
from app.models.model import VinProduit

def createVinProduit(cargo_id,vin):
    session = getSessionLocal()

    newVin = VinProduit(
        cargo_id = cargo_id,
        vin = vin
    )

    session.add(newVin)
    session.cre