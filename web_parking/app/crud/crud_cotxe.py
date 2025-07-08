from app.models import Cotxe, Client
from sqlalchemy.orm import Session

# crea un cotxe nou i l'afegeix a la base de dades
async def create_cotxe(
    db: Session,
    matricula: str,
    marca: str,
    model: str,
    color: str,
    any_matriculacio: int,
    imatge: str,
    dgt: str,
    combustible: str
):
    nou_cotxe = Cotxe(
        matricula=matricula,
        marca=marca,
        model=model,
        color=color,
        any_matriculacio=any_matriculacio,
        imatge=imatge,
        dgt=dgt,
        combustible=combustible
    )
    db.add(nou_cotxe)  # afegeix el cotxe a la sessio
    db.commit()         # confirma la transaccio
    db.refresh(nou_cotxe) # actualitza l'objecte amb la info de la db
    return nou_cotxe    # retorna el cotxe creat

# elimina un cotxe de la base de dades segons la matricula
async def delete_cotxe(db: Session, matricula: str):
    cotxe = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()  # busca el cotxe
    if cotxe:
        db.delete(cotxe)  # elimina el cotxe si existeix
        db.commit()       # confirma la eliminacio
    return cotxe         # retorna el cotxe eliminat o None si no existeix

# actualitza les dades d'un cotxe segons la matricula
async def update_cotxe(
    db: Session,
    matricula: str,
    marca: str = None,
    model: str = None,
    color: str = None,
    any_matriculacio: int = None,
    imatge: str = None,
    dgt: str = None,
    combustible: str = None
):
    cotxe = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()  # busca el cotxe
    if not cotxe:
        return None  # si no existeix, retorna None

    # actualitza cada camp només si s'ha passat un valor nou
    if marca is not None:
        cotxe.marca = marca
    if model is not None:
        cotxe.model = model
    if color is not None:
        cotxe.color = color
    if any_matriculacio is not None:
        cotxe.any_matriculacio = any_matriculacio
    if imatge is not None:
        cotxe.imatge = imatge
    if dgt is not None:
        cotxe.dgt = dgt
    if combustible is not None:
        cotxe.combustible = combustible

    db.commit()        # guarda els canvis a la base de dades
    db.refresh(cotxe)  # refresca l'objecte actualitzat
    return cotxe       # retorna el cotxe actualitzat

# obté un cotxe per la seva matricula
async def get_cotxe(db: Session, matricula: str):
    return db.query(Cotxe).filter(Cotxe.matricula == matricula).first()

# obté la llista de cotxes associats a un client per el seu dni
async def get_cotxes_by_client(db: Session, dni_usuari: str):
    client = db.query(Client).filter(Client.dni == dni_usuari).first()  # busca client
    if not client:
        return None  # si no existeix client, retorna None
    return client.cotxes  # retorna la llista de cotxes del client
