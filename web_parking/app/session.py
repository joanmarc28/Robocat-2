from itsdangerous import URLSafeSerializer
from fastapi import Request, Response
import os
from dotenv import load_dotenv
load_dotenv()

serializer = URLSafeSerializer(os.getenv("SECRET_KEY"))  # crea serializer per encriptar dades

def create_session_cookie(user_id: int) -> str:
    return serializer.dumps({"user_id": user_id})  # genera cookie segura amb id usuari

def get_user_from_cookie(request: Request):
    cookie = request.cookies.get("session")  # agafa cookie 'session' de la petició
    if cookie:
        try:
            data = serializer.loads(cookie)  # desxifra la cookie
            return data.get("user_id")  # retorna id usuari si existeix
        except Exception:
            return None  # si hi ha error (cookie manipulada), retorna None
    return None  # si no hi ha cookie, retorna None

def clear_session_cookie(response: Response):
    response.delete_cookie("session")  # elimina la cookie 'session' de la resposta
