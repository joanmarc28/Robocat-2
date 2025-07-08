from app.models import RoboCatRuta
from sqlalchemy.orm import Session

async def create_robocatruta(db: Session, **kwargs):
    r = RoboCatRuta(**kwargs)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

async def get_robocat_rutes(db: Session, id_robocat: int):
    return db.query(RoboCatRuta).filter(RoboCatRuta.id_robocat == id_robocat).all()

async def get_robocat_ruta(db: Session, assign_id: int):
    return db.query(RoboCatRuta).filter(RoboCatRuta.id == assign_id).first()

async def update_robocat_ruta(db: Session, assign_id: int, updates: dict):
    r = await get_robocat_ruta(db, assign_id)
    if not r:
        return None
    for k, v in updates.items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r

async def delete_robocat_ruta(db: Session, assign_id: int):
    r = await get_robocat_ruta(db, assign_id)
    if r:
        db.delete(r)
        db.commit()
    return r
