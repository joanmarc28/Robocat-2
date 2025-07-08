from fastapi import APIRouter, Form, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cotxe, Client
import json
from fastapi.responses import RedirectResponse
from sqlalchemy import select

router = APIRouter()  # crear router per gestionar les rutes relacionades amb cotxes

@router.post("/guardar-cotxe")
async def guardar_cotxe(
    matricula: str = Form(...),
    marca: str = Form(...),
    model: str = Form(...),
    color: str = Form(...),
    any_matriculacio: int = Form(...),
    imatge: str = Form(...),
    dgt: str = Form(...),
    combustible: str = Form(...),
    dni_usuari: str = Form(...), 
    db: Session = Depends(get_db)
):
    # comprovar si ja existeix un cotxe amb aquesta matricula
    cotxe_existent = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()
    if cotxe_existent:
        # si existeix, llençar error 400
        raise HTTPException(status_code=400, detail="Aquest cotxe ja existeix")

    # crear nou objecte Cotxe amb les dades rebudes
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
    # afegir el nou cotxe a la sessio de base de dades
    db.add(nou_cotxe)

    # buscar client pel dni per establir relacio
    client = db.query(Client).filter(Client.dni == dni_usuari).first()
    if not client:
        # si no troba client, llençar error 404
        raise HTTPException(status_code=404, detail="Client no trobat")

    # afegir el cotxe a la llista de cotxes del client (relacio)
    client.cotxes.append(nou_cotxe) 
    # confirmar canvis a la base de dades
    db.commit()
    # refrescar el nou cotxe per obtenir dades actualitzades
    db.refresh(nou_cotxe)

    # retornar missatge d'exit amb dades del cotxe
    return {
        "message": "Cotxe guardat correctament i vinculat al client!",
        "cotxe": {
            "matricula": nou_cotxe.matricula,
            "marca": nou_cotxe.marca,
            "model": nou_cotxe.model,
            "color": nou_cotxe.color,
            "any_matriculacio": nou_cotxe.any_matriculacio,
            "imatge": nou_cotxe.imatge,
            "dgt": nou_cotxe.dgt,
            "combustible": nou_cotxe.combustible
        }
    }


@router.get("/obtenir-cotxe")
def obtenir_cotxe(
    matricula: str,
    dni: str,
    db: Session = Depends(get_db)
):
    # consultar cotxe i client associat mitjançant join i filtratge per matricula i dni client
    cotxe = (
        db.query(Cotxe)
        .join(Cotxe.clients)
        .filter(Cotxe.matricula == matricula, Client.dni == dni)
        .first()
    )

    # si no es troba el cotxe amb aquest client, llençar error 404
    if not cotxe:
        raise HTTPException(status_code=404, detail="Cotxe no trobat per aquest client")

    # retornar les dades del cotxe trobat
    return {
        "matricula": cotxe.matricula,
        "marca": cotxe.marca,
        "model": cotxe.model,
        "color": cotxe.color,
        "any_matriculacio": cotxe.any_matriculacio,
        "imatge": cotxe.imatge,
        "dgt": cotxe.dgt,
        "combustible": cotxe.combustible
    }


# eliminar cotxe
@router.post("/eliminar-cotxe")
async def eliminar_cotxe(request: Request, db: Session = Depends(get_db)):
    # obtenir dades json del request
    data = await request.json()
    # agafar matricula per identificar cotxe
    matricula = data.get("matricula")

    # buscar cotxe per matricula
    cotxe = db.query(Cotxe).filter(Cotxe.matricula == matricula).first()
    if cotxe:
        # si existeix, eliminar-lo de la base de dades
        db.delete(cotxe)
        db.commit()
        # retornar missatge d'exit
        return {"success": True, "message": f"Cotxe {matricula} eliminat"}
    # si no es troba cotxe, retornar error
    return {"success": False, "error": "Cotxe no trobat"}
