from app.config.database import getSessionLocal
from app.models.test import Cargo
from decimal import Decimal

def getAllByManifest(manifest_id):
    session = getSessionLocal()
    cargos = session.query(Cargo).filter_by(manifest_id = manifest_id).all()
    session.close()
    return cargos 
    

def createCargo(bl_no,manifest_id,shipper_id,consigne_id,description,weight,mesurement):
    session = getSessionLocal()
    
    newCargo = Cargo(
        bl_no = bl_no,
        manifest_id = manifest_id,
        shipper_id = shipper_id,
        consigne_id = consigne_id,
        description_good = description,
        weight = Decimal(weight),
        measurement = Decimal(mesurement)
    )

    session.add(newCargo)
    session.commit()
    session.close()