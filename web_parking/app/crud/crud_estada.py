from app.models import Estada
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# crea una nova estada amb els detalls especificats i l'afegeix a la base de dades
async def create_estada(
    db: Session,
    dni_usuari: str,
    matricula_cotxe: str,
    id_zona: int,
    data_inici: datetime,
    data_final: datetime,
    durada: timedelta,
    preu: float,
    activa: bool
):
    nova_estada = Estada(
        dni_usuari=dni_usuari,
        matricula_cotxe=matricula_cotxe,
        id_zona=id_zona,
        data_inici=data_inici,
        data_final=data_final,
        durada=durada,
        preu=preu,
        activa=activa
    )
    db.add(nova_estada)  # afegeix l'estada nova a la sessio
    db.commit()          # confirma la transaccio
    db.refresh(nova_estada)  # refresca l'objecte amb la info de la db
    return nova_estada   # retorna l'estada creada

# obté una estada per la seva id
async def get_estada(db: Session, estada_id: int):
    return db.query(Estada).filter(Estada.id == estada_id).first()  # busca i retorna l'estada o None

# obté totes les estades d'un client segons el seu dni
async def get_estades_by_client(db: Session, dni_usuari: str):
    return db.query(Estada).filter(Estada.dni_usuari == dni_usuari).all()  # retorna llista d'estades

# actualitza una estada amb els camps especificats al diccionari updates
async def update_estada(db: Session, estada_id: int, updates: dict):
    estada = get_estada(db, estada_id)  # busca l'estada
    if not estada:
        return None  # si no existeix retorna None
    for key, value in updates.items():  # actualitza cada atribut
        setattr(estada, key, value)
    db.commit()       # confirma els canvis
    db.refresh(estada)  # refresca l'objecte
    return estada     # retorna l'estada actualitzada

# elimina una estada per la seva id
async def delete_estada(db: Session, estada_id: int):
    estada = get_estada(db, estada_id)  # busca l'estada
    if estada:
        db.delete(estada)  # elimina l'estada si existeix
        db.commit()       # confirma la eliminacio
    return estada        # retorna l'estada eliminada o None
