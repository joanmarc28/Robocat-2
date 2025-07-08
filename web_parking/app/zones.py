from fastapi import APIRouter, Form, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Zona, Estada, Policia, Usuari, Client, Cotxe
import json
from fastapi.responses import RedirectResponse
from app.session import get_user_from_cookie
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.post("/guardar-zona")
async def guardar_zona(
    request: Request,
    tipus: str = Form(...),
    temps_Maxim: int = Form(0),
    preu_Min: float = Form(...),
    ciutat: str = Form(...),
    carrer: str = Form(...),
    coords: str = Form(...),
    db: Session = Depends(get_db)
):
    # validacio coords: comprovem que coords son un json correcte
    try:
        import json
        coordenades_data = json.loads(coords)
    except Exception as e:
        raise HTTPException(status_code=400, detail="coordenades mal formatejades")

    nova_zona = Zona(
        tipus=tipus,
        ciutat=ciutat,
        carrer=carrer,
        preu_min=preu_Min,
        temps_maxim=temps_Maxim,
        coordenades=json.dumps(coordenades_data)  # guardem les coords com a string json
    )

    db.add(nova_zona)
    db.commit()
    db.refresh(nova_zona)

    return {
        "message": "zona guardada correctament!",
        "zona": {
            "id": nova_zona.id,
            "tipus": nova_zona.tipus,
            "carrer": nova_zona.carrer,
            "temps_maxim": nova_zona.temps_maxim,
            "preu_min": float(nova_zona.preu_min),
            "coordenades": nova_zona.coordenades
        }
    }


@router.get("/obtenir-zones")
def obtenir_zones(ciutat: str = None, db: Session = Depends(get_db)):
    # si tenim ciutat, filtrem per aquesta, si no, retornem totes les zones
    if ciutat:
        zones = db.query(Zona).filter(Zona.ciutat == ciutat).all()
    else:
        zones = db.query(Zona).all()

    result = []
    for zona in zones:
        result.append({
            "id": zona.id,
            "tipus": zona.tipus,
            "temps_maxim": zona.temps_maxim,
            "preu_min": float(zona.preu_min),
            "carrer": zona.carrer,
            "coordenades": json.loads(zona.coordenades)  # convertim string json a objecte
        })
    return result

@router.post("/eliminar_zona")
async def eliminar_zona(request: Request, db: Session = Depends(get_db)):
    # obtenim id zona del json enviat i intentem eliminar-la
    data = await request.json()
    zona_id = data.get("id")

    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if zona:
        db.delete(zona)
        db.commit()
        return {"success": True}
    return {"success": False, "error": "zona no trobada"}

@router.post("/guardar-estada")
async def guardar_estada(
    dni_usuari: str = Form(...),
    matricula_cotxe: str = Form(...),
    id_zona: int = Form(...),
    data_inici: str = Form(...),
    data_final: str = Form(None),
    preu: float = Form(...),
    activa: bool = Form(...),
    db: Session = Depends(get_db)
):
    # creem nova estada amb les dades rebudes
    nova_estada = Estada(
        dni_usuari=dni_usuari,
        matricula_cotxe=matricula_cotxe,
        id_zona=id_zona,
        data_inici=data_inici,
        data_final=data_final,
        preu=preu,
        activa=activa
    )

    db.add(nova_estada)
    db.commit()
    db.refresh(nova_estada)

    return {
        "message": "estada registrada correctament!",
        "estada": {
            "id": nova_estada.id,
            "dni_usuari": nova_estada.dni_usuari,
            "matricula_cotxe": nova_estada.matricula_cotxe,
            "id_zona": nova_estada.id_zona,
            "data_inici": nova_estada.data_inici,
            "data_final": nova_estada.data_final,
            "preu": float(nova_estada.preu),
            "activa": nova_estada.activa
        }
    }
