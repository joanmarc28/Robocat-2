from fastapi import FastAPI, Request, Depends, Form, Response, HTTPException
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form, Request
from fastapi.responses import RedirectResponse
import json
from google.cloud import vision
import base64
import io
from fastapi.responses import JSONResponse
import requests
from passlib.context import CryptContext
from app import auth, zones, cars, assistent, dashboard_robots, infraccio
from app.database import Base, engine
from app.session import get_user_from_cookie
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Usuari,Policia, Client, Cotxe, Estada, Zona
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")  # monta la carpeta static per servir fitxers estatics

templates = Jinja2Templates(directory="app/templates")  # carpeta on hi ha les plantilles jinja2

load_dotenv()  # carrega variables d'entorn des del fitxer .env
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/robocat-user-app-5d2b35bd5c22.json"  # clau api google vision

Base.metadata.create_all(bind=engine)  # crea les taules de la base de dades si no existeixen

app.include_router(auth.router)  # registra les rutes d'autenticacio
app.include_router(zones.router)  # registra les rutes de zones
app.include_router(cars.router)  # registra les rutes de cotxes
app.include_router(assistent.router)  # registra les rutes de l'assistent
app.include_router(dashboard_robots.router)  # registra les rutes del dashboard robots
app.include_router(infraccio.router)  # registra les rutes de infraccions

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)  # agafa l'id usuari de la cookie
    if not user_id:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user_id": user_id,
            "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
        })

    return RedirectResponse(url="/welcome", status_code=303)  # si esta loguejat redirigeix a welcome

@app.get("/welcome")
def welcome(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)  # agafa l'id usuari de la cookie
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)  # si no esta loguejat, a login

    user = db.query(Usuari).get(user_id)  # agafa usuari per id
    role = "client"
    if db.query(Policia).filter_by(user_id=user.id).first():  # comprova si es policia
        role = "policia"

    estada_activa = None
    if role == "client":
        estada_activa = db.query(Estada).filter_by(dni_usuari=user.client.dni, activa=True).first()  # agafa estada activa si es client

    return templates.TemplateResponse("welcome.html", {
        "request": request,
        "user_id": user_id,
        "role": role,
        "user": user,
        "estada_activa": estada_activa,
        "datetime": datetime  # passem el mòdul datetime per usar a la plantilla
    })

@app.get("/parking")
def parking(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)  # agafa l'id usuari de la cookie
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)  # si no esta loguejat, a login

    user = db.query(Usuari).get(user_id)  # agafa usuari per id
    client = db.query(Client).filter_by(user_id=user.id).first()  # agafa client per usuari
    if not client:
        return RedirectResponse(url="/welcome", status_code=303)  # si no es client, redirigeix a welcome

    any_actual = datetime.now().year  # any actual

    return templates.TemplateResponse("parking.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "client": client,
        "any_actual": any_actual,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

@app.get("/zones")
def parking(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)  # agafa l'id usuari de la cookie
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)  # si no esta loguejat, a login

    user = db.query(Usuari).get(user_id)  # agafa usuari per id
    if db.query(Client).filter_by(user_id=user.id).first():  # si es client, redirigeix a welcome
        return RedirectResponse(url="/welcome", status_code=303)

    role = "policia"  # si no es client, es policia
    return templates.TemplateResponse("zones.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "role": role,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

@app.get("/cars")
def cars(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)  # agafa l'id usuari de la cookie

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)  # si no esta loguejat, redirigeix a login

    user = db.query(Usuari).get(user_id)  # agafa usuari per id
    if db.query(Policia).filter_by(user_id=user.id).first():
        return RedirectResponse(url="/welcome", status_code=303)  # si es policia, redirigeix a welcome

    client = db.query(Client).filter_by(user_id=user.id).first()  # agafa client per usuari

    cotxes = []
    print(f"client: {client}")  # debug client
    print(f"cotxes del client: {client.cotxes}")  # debug cotxes
    for cotxe in client.cotxes:
        image_link = cercar_imatges(f"{cotxe.marca} {cotxe.model} {cotxe.color} {cotxe.any_matriculacio}")  # busca imatge
        cotxes.append({
            "matricula": cotxe.matricula,
            "model": cotxe.model,
            "marca": cotxe.marca,
            "any": cotxe.any_matriculacio,
            "color": cotxe.color,
            "combustible": cotxe.combustible,
            "dgt": cotxe.dgt,
            "image_car": image_link
        })

    return templates.TemplateResponse("cars.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "client": client,
        "cotxes": cotxes
    })

@app.get("/deteccio", response_class=HTMLResponse)
async def mostra_deteccio(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)  # agafa l'id usuari de la cookie
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)  # si no esta loguejat, a login

    user = db.query(Usuari).get(user_id)  # agafa usuari per id
    if db.query(Client).filter_by(user_id=user.id).first():  # si es client, redirigeix a welcome
        return RedirectResponse(url="/welcome", status_code=303)

    role = "policia"  # si no es client, es policia
    return templates.TemplateResponse("deteccio.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "role": role
    })

@app.post("/extract-plate")
async def analitzar_matricula(capturedImage: str = Form(...)):
    try:
        image_data = base64.b64decode(capturedImage.split(",")[1])  # decodifica la imatge base64
        client = vision.ImageAnnotatorClient()  # client google vision
        image = vision.Image(content=image_data)  # crea imatge per google vision
        response = client.text_detection(image=image)  # detecta text

        texts = response.text_annotations
        if texts:
            text_detected = texts[0].description.strip().replace("\n", "")  # neteja text detectat
        else:
            text_detected = ""

        return JSONResponse(content={"plate": text_detected})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)  # error

def cercar_imatges(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'cx': os.getenv("CSE_ID"),
        'key': os.getenv("API_KEY"),
        'searchType': 'image',
        'num': 1
    }
    print(f"buscant: {query}")  # debug query
    response = requests.get(url, params=params)
    print("url final:", response.url)  # debug url
    print("codi resposta:", response.status_code)  # debug codi resposta
    print("resposta:", response.text)  # debug resposta completa

    if response.status_code == 200:
        resultats = response.json().get('items', [])
        return resultats[0]['link'] if resultats else None  # retorna link de la imatge si hi ha resultats
    return None  # retorna none si falla

@app.get("/historial")
def veure_historial(request: Request, db: Session = Depends(get_db)):

    user_id = get_user_from_cookie(request)  # agafa l'id usuari de la cookie
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)  # si no esta loguejat, redirigeix a login

    usuari = db.query(Usuari).get(user_id)  # agafa usuari per id
    if db.query(Policia).filter_by(user_id=usuari.id).first():
        return RedirectResponse(url="/welcome", status_code=303)  # si es policia, redirigeix a welcome

    estades = db.query(Estada).filter(Estada.dni_usuari == usuari.client.dni).all()  # agafa totes les estades del client
    client = db.query(Client).filter_by(user_id=usuari.id).first()  # agafa client per usuari

    dades = []
    for estada in estades:
        zona = db.query(Zona).filter(Zona.id == estada.id_zona).first()  # agafa zona per estada
        cotxe = db.query(Cotxe).filter_by(matricula=estada.matricula_cotxe).first()  # agafa cotxe per matricula
        image_link = cercar_imatges(f"{cotxe.marca} {cotxe.model} {cotxe.color} {cotxe.any_matriculacio}")  # busca imatge cotxe

        dades.append({
            "id": estada.id,
            "data_inici": estada.data_inici,
            "data_final": estada.data_final,
            "matricula": estada.matricula_cotxe,
            "zona": zona.tipus,
            "carrer": zona.carrer,
            "ciutat": zona.ciutat,
            "preu": estada.preu,
            "activa": estada.activa,
            "image_car": image_link
        })
    dades.reverse()  # posa l'historial en ordre invers

    return templates.TemplateResponse("historial.html", {
        "request": request,
        "estades": dades,
        "user_id": user_id,
        "user": usuari,
        "client": client
    })

@app.post("/finalitzar-estada")
async def finalitzar_estada(estada_id: int = Form(...), db: Session = Depends(get_db)):
    estada = db.query(Estada).filter(Estada.id == estada_id).first()  # agafa estada per id
    if not estada:
        raise HTTPException(status_code=404, detail="estada no trobada")  # si no troba estada, error 404

    estada.activa = False  # marca estada com a no activa
    db.commit()  # guarda canvis

    return RedirectResponse(url="/historial", status_code=303)  # redirigeix a historial

