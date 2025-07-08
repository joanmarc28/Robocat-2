from app.models import Infraccio
from sqlalchemy.orm import Session

async def create_infraccio(db: Session, **kwargs):
    infraccio = Infraccio(**kwargs)
    db.add(infraccio)
    db.commit()
    db.refresh(infraccio)
    return infraccio

async def get_infraccio(db: Session, infraccio_id: int):
    return db.query(Infraccio).filter(Infraccio.id == infraccio_id).first()

async def get_infraccions_by_matricula(db: Session, matricula: str):
    return db.query(Infraccio).filter(Infraccio.matricula_cotxe == matricula).all()

async def update_infraccio(db: Session, infraccio_id: int, updates: dict):
    infraccio = await get_infraccio(db, infraccio_id)
    if not infraccio:
        return None
    for key, value in updates.items():
        setattr(infraccio, key, value)
    db.commit()
    db.refresh(infraccio)
    return infraccio

async def delete_infraccio(db: Session, infraccio_id: int):
    infraccio = await get_infraccio(db, infraccio_id)
    if infraccio:
        db.delete(infraccio)
        db.commit()
    return infraccio
