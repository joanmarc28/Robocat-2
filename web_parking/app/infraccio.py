from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends,Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Robot, Policia, PossibleInfraccio, Infraccio, Usuari, Client
from datetime import datetime
import json
import requests
import copy
import os
from dotenv import load_dotenv
from app.session import get_user_from_cookie
from fastapi.responses import RedirectResponse

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/infraccions")
def veure_infraccions(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    usuari = db.query(Usuari).get(user_id)
    policia = db.query(Policia).filter_by(user_id=usuari.id).first()
    client = db.query(Client).filter_by(user_id=usuari.id).first()

    role = "client"
    possibles_list = []
    infractors_list = []

    if policia:
        role = "policia"
        possibles = db.query(PossibleInfraccio).all()
        infraccions = db.query(Infraccio).all()

        possibles_list = [{
            "matricula": p.matricula_cotxe,
            "infraccio": p.descripcio,
            "timestamp": p.data_posinfraccio,
            "imatge": p.imatge
        } for p in possibles]

        infractors_list = [{
            "nom": db.query(Usuari).join(Client).filter(Client.dni == i.dni_usuari).first().email.split("@")[0],
            "dni": i.dni_usuari,
            "matricula": i.matricula_cotxe,
            "data": i.data_infraccio,
            "import": i.preu,
            "infraccio": i.descripcio,
            "imatge": i.imatge
        } for i in infraccions]

    elif client:
        infraccions = db.query(Infraccio).filter_by(dni_usuari=client.dni).all()
        infractors_list = [{
            "nom": usuari.email.split("@")[0],
            "dni": i.dni_usuari,
            "matricula": i.matricula_cotxe,
            "data": i.data_infraccio,
            "import": i.preu,
            "infraccio": i.descripcio,
            "imatge": i.imatge
        } for i in infraccions]

    return templates.TemplateResponse("infraccions.html", {
        "request": request,
        "user_id": user_id,
        "user": usuari,
        "role": role,
        "possibles_infractors": possibles_list,
        "infractors": infractors_list
    })


@router.post("/infraccions")
def gestionar_infraccio(
    request: Request,
    accio: str = Form(...),
    matricula: str = Form(None),
    timestamp: str = Form(None),
    dni: str = Form(None),
    data: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id = get_user_from_cookie(request)
    if not user_id:
        raise HTTPException(status_code=403, detail="Accés no autoritzat")

    usuari = db.query(Usuari).get(user_id)
    es_policia = db.query(Policia).filter_by(user_id=usuari.id).first()

    # ✅ Només policies poden eliminar infraccions
    if accio == "eliminar":
        if not es_policia:
            raise HTTPException(status_code=403, detail="Només policies poden eliminar infraccions")

        if matricula and timestamp:
            db.query(PossibleInfraccio).filter_by(matricula_cotxe=matricula, data_posinfraccio=timestamp).delete()
            db.commit()

        elif dni and data:
            db.query(Infraccio).filter_by(dni_usuari=dni, data_infraccio=data).delete()
            db.commit()

    return RedirectResponse(url="/infraccions", status_code=303)



# Funció per verificar si l'usuari és policia
def verifica_policia(request: Request, db: Session):
    user_id = get_user_from_cookie(request)
    if not user_id:
        raise HTTPException(status_code=403, detail="Accés denegat")

    usuari = db.query(Usuari).get(user_id)
    policia = db.query(Policia).filter_by(user_id=usuari.id).first()
    if not policia:
        raise HTTPException(status_code=403, detail="Només policies poden afegir infraccions")

    return user_id,usuari

@router.post("/afegir-infraccio")
async def afegir_infraccio(
    request: Request,
    dni: str = Form(...),
    matricula: str = Form(...),
    zona: int = Form(...),
    data: str = Form(...),  # format: 2025-06-24T14:30
    infraccio: str = Form(...),
    preu: float = Form(...),
    imatge: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id, usuari = verifica_policia(request, db)

    try:
        data_parsed = datetime.strptime(data, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de data invàlid")

    nova = Infraccio(
        dni_usuari=dni,
        matricula_cotxe=matricula,
        id_zona=zona,
        data_infraccio=data_parsed,
        descripcio=infraccio,
        preu=preu,
        imatge=imatge
    )

    db.add(nova)

    # Elimina la PossibleInfracció si existeix
    db.query(PossibleInfraccio).filter_by(
        matricula_cotxe=matricula,
        data_posinfraccio=data_parsed
    ).delete()

    db.commit()
    
    deleted = db.query(PossibleInfraccio).filter_by(
        matricula_cotxe=matricula,
        data_posinfraccio=data_parsed
    ).delete()

    print(f"🔍 PossibleInfraccio eliminada: {deleted} registre(s)")  # opcional
    return RedirectResponse(url="/infraccions?success=1", status_code=303)

@router.get("/nova_infraccio")
def afegir_infraccio_form(request: Request, matricula: str, timestamp: str, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    usuari = db.query(Usuari).get(user_id)
    if not db.query(Policia).filter_by(user_id=usuari.id).first():
        return RedirectResponse(url="/welcome", status_code=303)

    # Busca la possible infracció
    possible = db.query(PossibleInfraccio).filter_by(matricula_cotxe=matricula, data_posinfraccio=timestamp).first()
    if not possible:
        raise HTTPException(status_code=404, detail="Possible infracció no trobada")

    # Intenta recuperar el client pel cotxe
    client = db.query(Client).join(Client.cotxes).filter_by(matricula=matricula).first()
    dni = client.dni if client else ""

    return templates.TemplateResponse("nova_infraccio.html", {
        "request": request,
        "matricula": matricula,
        "timestamp": timestamp,
        "descripcio": possible.descripcio,
        "imatge": possible.imatge,
        "dni": dni,
        "data": possible.data_posinfraccio.strftime("%Y-%m-%dT%H:%M")  # pel <input type=datetime-local>
    })
