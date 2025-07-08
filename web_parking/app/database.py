from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # carrega les variables d'entorn del fitxer .env

DB_USER = os.getenv("DB_USER")  
DB_PASSWORD = os.getenv("DB_PASSWORD")  
DB_NAME = os.getenv("DB_NAME")  
DB_HOST = os.getenv("DB_HOST")  
DB_PORT = os.getenv("DB_PORT", 5432) 

# crea la url de connexio a la base de dades postgresql
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)  # crea l'engine de connexio a la db
# crea la sessio local per fer operacions a la db (sense autocommit ni autoflush automatics)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # base declarativa per definir models ORM

# funcio generator per obtenir una sessio db i tancar-la automaticament
def get_db():
    db = SessionLocal()  # crea una nova sessio
    try:
        yield db  # retorna la sessio per fer queries
    finally:
        db.close()  # assegura que la sessio es tanqui quan acabi l'operacio
