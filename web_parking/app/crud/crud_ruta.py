from app.models import Ruta
from app.models import PuntRuta
from sqlalchemy.orm import Session

async def create_ruta(db: Session, **kwargs):
    r = Ruta(**kwargs)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

async def get_ruta(db: Session, ruta_id: int):
    return db.query(Ruta).filter(Ruta.id == ruta_id).first()

async def get_rutes_by_policia(db: Session, id_policia: int):
    return db.query(Ruta).filter(Ruta.id_policia == id_policia).all()

async def update_ruta(db: Session, ruta_id: int, updates: dict):
    r = await get_ruta(db, ruta_id)
    if not r:
        return None
    for k, v in updates.items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r

async def delete_ruta(db: Session, ruta_id: int):
    r = await get_ruta(db, ruta_id)
    if r:
        db.delete(r)
        db.commit()
    return r

async def create_puntruta(db: Session, **kwargs):
    p = PuntRuta(**kwargs)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

async def get_punts_by_ruta(db: Session, id_ruta: int):
    return db.query(PuntRuta).filter(PuntRuta.id_ruta == id_ruta).order_by(PuntRuta.ordre).all()