from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta  # importa timedelta per fer calculs de temps
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # directori base del projecte
sys.path.append(BASE_DIR)  # afegeix el directori base al path per importar mòduls

from app.database import engine, SessionLocal
from app.models import Estada, Robot


def actualitzar_estades():
    db = SessionLocal()  # crea sessió de base de dades
    try:
        ara = datetime.utcnow()  # data i hora actual en utc
        estades = db.query(Estada).filter(Estada.activa == True).all()  # agafa estades actives
        for estada in estades:
            if estada.data_final and estada.data_final <= ara:
                print(f"[{ara}] estada {estada.id} expirada, desactivant.")  # debug estada expirada
                estada.activa = False  # desactiva estada
            else:
                temps_restant = estada.data_final - ara if estada.data_final else None  # calcula temps restant
                print(f"[{ara}] estada {estada.id} encara activa. temps restant: {temps_restant}")  # debug estada activa

        # robots (si fa +2 minuts de l'ultima connexio -> offline)
        robots = db.query(Robot).filter(Robot.estat == "online").all()  # agafa robots online
        for robot in robots:
            if robot.ultima_connexio and robot.ultima_connexio < ara - timedelta(minutes=2):
                print(f"[{ara}] robot {robot.identificador} sembla desconnectat. marcant com offline.")  # debug robot offline
                robot.estat = "offline"  # marca robot com offline

        db.commit()  # guarda canvis a la base de dades
    except Exception as e:
        print(f"error: {e}")  # captura i mostra error
    finally:
        db.close()  # tanca sessió


if __name__ == "__main__":
    actualitzar_estades()  # executa la funció principal
