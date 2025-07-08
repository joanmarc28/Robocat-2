from app.models import PossibleInfraccio
from sqlalchemy.orm import Session

async def create_possible_infraccio(db: Session, **kwargs):
    p = PossibleInfraccio(**kwargs)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

async def get_possible_infraccio(db: Session, pid: str):
    return db.query(PossibleInfraccio).filter(PossibleInfraccio.id == pid).first()

async def get_possibles_by_matricula(db: Session, matricula: str):
    return db.query(PossibleInfraccio).filter(PossibleInfraccio.matricula_cotxe == matricula).all()

async def delete_possible_infraccio(db: Session, pid: str):
    p = await get_possible_infraccio(db, pid)
    if p:
        db.delete(p)
        db.commit()
    return p

async def update_possible_infraccio(db: Session, pid: str, updates: dict):
    p = await get_possible_infraccio(db, pid)
    if not p:
        return None
    for key, value in updates.items():
        setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return p
