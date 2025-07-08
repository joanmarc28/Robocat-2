from fastapi import APIRouter, Response, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.crud_users import create_user
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from app.models import Usuari,Policia, Client
from app.session import create_session_cookie, get_user_from_cookie, clear_session_cookie
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
#mail api 
import requests
from email.mime.text import MIMEText
import pickle
import os
import base64

router = APIRouter()  # crear router per les rutes de l'aplicacio
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # configurar hash per contrasenyes
templates = Jinja2Templates(directory="app/templates")  # configurar templates jinja2

# configuracio gmail api
MAILGUN_DOMAIN = 'sandbox2ec3eca2b5c848e58adabcbf4537d632.mailgun.org'  # domini mailgun per enviar emails

# carregar variables d'entorn del fitxer .env
load_dotenv()

# agafar la clau api de l'entorn
MAILGUN_API_KEY = os.getenv("GEMINI_API_KEY")

@router.post("/registre")
async def processar_registre(
    email: str = Form(...),
    password: str = Form(...),
    data_naixement: str = Form(...),
    ciutat: str = Form(...),
    pais: str = Form(...),
    es_policia: bool = Form(False),
    dni: str = Form(None),
    nom: str = Form(None),
    cognoms: str = Form(None),
    direccio: str = Form(None),
    codi_postal: str = Form(None),
    telefon: str = Form(None),
    placa: str = Form(None),
    db: Session = Depends(get_db)
):
    # crear usuari nou amb dades i contrasenya hashed
    await create_user(
        db=db,
        email=email,
        password=pwd_context.hash(password),
        data_naixement=data_naixement,
        ciutat=ciutat,
        pais=pais,
        es_policia=es_policia,
        dni=dni,
        nom=nom,
        cognoms=cognoms,
        direccio=direccio,
        codi_postal=codi_postal,
        telefon=telefon,
        placa=placa
    )
    # redirigir a la pagina de login
    return RedirectResponse(url="/login", status_code=303)

@router.get("/login")
def parking(request: Request):
    # mostrar template de login
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@router.get("/registre")
def parking(request: Request):
    # agafar usuari de la cookie per veure si esta loguejat
    user_id = get_user_from_cookie(request)
    if user_id:
        # si ja esta loguejat, redirigir a welcome
        return RedirectResponse(url="/welcome", status_code=303)

    # si no, mostrar formulari de registre
    return templates.TemplateResponse("registre.html", {
        "request": request
    })

@router.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # buscar usuari per email
    user = db.query(Usuari).filter(Usuari.email == email).first()
    # verificar que usuari existeix i contrasenya coincideix
    if not user or not pwd_context.verify(password, user.password):
        # si no, redirigir a login amb error
        return RedirectResponse(url="/login?error=1", status_code=303)
    
    # crear cookie de sessio per usuari
    session_cookie = create_session_cookie(user.id)
    # redirigir a welcome i posar cookie de sessio al response
    response = RedirectResponse(url="/welcome", status_code=303)
    response.set_cookie(key="session", value=session_cookie, httponly=True)
    return response

@router.get("/logout")
def logout():
    # crear response per redirigir a login
    response = RedirectResponse(url="/login", status_code=303)
    # esborrar cookie de sessio
    clear_session_cookie(response)
    return response

@router.post("/recuperar_contrasenya")
async def recover_password(email: str = Form(...)):
    try:
        # crear link de recuperacio de contrasenya
        recovery_link = f"https://robocat.jmprojects.cat/reset-password?email={email}"
        # enviar email de recuperacio
        result = send_recovery_email(email, recovery_link)
        # redirigir a login amb missatge d'enviat
        return RedirectResponse("/login?msg=recovery_sent", status_code=303)
    except Exception as e:
        # en cas d'error, llençar excepcio 500 amb detall
        raise HTTPException(status_code=500, detail=f"Error enviant correu: {e}")

@router.get("/recuperar_contrasenya", response_class=HTMLResponse)
def recuperar_contrasenya_form(request: Request):
    # mostrar template per recuperar contrasenya
    return templates.TemplateResponse("recuperar_contrasenya.html", {"request": request})

def send_recovery_email(to_email, recovery_link):
    # configurar contingut del email de recuperacio
    subject = "Recuperació de contrasenya"
    text_content = f"""
    Hola,

    Has demanat recuperar la teva contrasenya. Fes clic al següent enllaç per reiniciar-la:
    {recovery_link}

    Si no ho has demanat, ignora aquest missatge.
    """

    # fer peticio POST a mailgun per enviar email
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Robocat <postmaster@{MAILGUN_DOMAIN}>",
            "to": to_email,
            "subject": subject,
            "text": text_content
        }
    )

    # comprovar que la resposta es correcta
    if response.status_code != 200:
        # si no, llençar excepcio amb el text d'error
        raise Exception(f"Mailgun error: {response.text}")

    return response.json()

@router.get("/perfil")
def welcome(request: Request, db: Session = Depends(get_db)):
    # agafar usuari de cookie
    user_id = get_user_from_cookie(request)
    if not user_id:
        # si no hi ha usuari, redirigir a login
        return RedirectResponse(url="/login", status_code=303)

    # obtenir usuari de la base de dades
    user = db.query(Usuari).get(user_id)
    # comprovar si usuari es policia
    policia = db.query(Policia).filter_by(user_id=user.id).first()
    # obtenir client associat a usuari
    client = db.query(Client).filter_by(user_id=user.id).first()

    if policia:
        # si es policia, redirigir a welcome
        return RedirectResponse(url="/welcome", status_code=303)

    # mostrar template perfil amb dades d'usuari i client
    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "client": client
    })
    

@router.post("/perfil/update")
def update_perfil(
    request: Request,
    email: str = Form(...),
    data_naixement: str = Form(...),
    ciutat: str = Form(...),
    pais: str = Form(None),
    nom: str = Form(...),
    cognoms: str = Form(None),
    direccio: str = Form(None),
    codi_postal: str = Form(None),
    telefon: str = Form(None),
    db: Session = Depends(get_db)
):
    # agafar usuari de la cookie
    user_id = get_user_from_cookie(request)
    if not user_id:
        # si no hi ha usuari, redirigir a login
        return RedirectResponse(url="/login", status_code=303)

    # obtenir usuari de la base de dades
    user = db.query(Usuari).get(user_id)
    if not user or not user.client:
        # si no existeix usuari o client, redirigir a login
        return RedirectResponse(url="/login", status_code=303)

    # actualitzar dades de l'usuari
    user.email = email
    user.data_naixement = data_naixement
    user.ciutat = ciutat
    user.pais = pais

    # actualitzar dades del client associat
    client = user.client
    client.nom = nom
    client.cognoms = cognoms
    client.direccio = direccio
    client.codi_postal = codi_postal
    client.telefon = telefon

    # guardar canvis a la base de dades
    db.commit()
    # redirigir a la pagina de perfil
    return RedirectResponse(url="/perfil", status_code=303)
