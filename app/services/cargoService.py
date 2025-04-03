from app.config.database import getSessionLocal
from app.models.model import Cargo
from decimal import Decimal
from app.services.rechercheService import sont_presque_pareils
from datetime import datetime

def getAllByManifest(manifest_id):
    session = getSessionLocal()
    cargos = session.query(Cargo).filter_by(manifest_id = manifest_id).all()
    session.close()
    return cargos 
    

def createCargo(voyage_id,port_depart,date_depart,shipper,consigne,bl_no,poid,volume):
    session = getSessionLocal()
    
    newCargo = Cargo(
        voyage_id = voyage_id,
        bl_no = bl_no,
        port_depart = port_depart,
        date_depart = datetime.strptime(date_depart, "%Y-%m-%d").date(),
        shipper = shipper,
        consigne = consigne,
        weight = Decimal(poid),
        measurement = Decimal(volume)
    )

    session.add(newCargo)
    session.commit()
    session.refresh(newCargo)
    session.close()
    return newCargo

def getCargoByBL(bl_no):
    session = getSessionLocal()
    cargo = session.query(Cargo).filter_by(bl_no = bl_no).first()
    session.close()
    return cargo
