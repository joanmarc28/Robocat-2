from app.models import Zona
from sqlalchemy.orm import Session

# crea una nova zona de aparcament amb les dades indicades
async def create_zona(db: Session, tipus: str, ciutat: str, carrer: str, preu_min: float, temps_maxim: int, coordenades: str):
    nova_zona = Zona(
        tipus=tipus,
        ciutat=ciutat,
        carrer=carrer,
        preu_min=preu_min,
        temps_maxim=temps_maxim,
        coordenades=coordenades
    )
    db.add(nova_zona)  # afegeix la nova zona a la sessio
    db.commit()        # confirma la transaccio a la base de dades
    db.refresh(nova_zona)  # refresca l'objecte zona amb la info de la db
    return nova_zona  # retorna la zona creada

# obté una zona segons el seu id
async def get_zona(db: Session, zona_id: int):
    return db.query(Zona).filter(Zona.id == zona_id).first()

# obté totes les zones disponibles
async def get_all_zones(db: Session):
    return db.query(Zona).all()

# actualitza una zona existent amb les dades passades en un diccionari
async def update_zona(db: Session, zona_id: int, updates: dict):
    zona = get_zona(db, zona_id)  # obté la zona per id
    if not zona:
        return None
    for key, value in updates.items():  # assigna cada camp del diccionari a la zona
        setattr(zona, key, value)
    db.commit()  # confirma els canvis
    db.refresh(zona)  # refresca l'objecte zona amb els canvis
    return zona  # retorna la zona actualitzada

# elimina una zona segons el seu id
async def delete_zona(db: Session, zona_id: int):
    zona = get_zona(db, zona_id)  # obté la zona per id
    if zona:
        db.delete(zona)  # elimina la zona de la sessio
        db.commit()      # confirma l'eliminacio
    return zona  # retorna la zona eliminada (o None si no existeix)
