from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Boolean,
    DECIMAL, Interval, TIMESTAMP, Table, DateTime
)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

possessio_table = Table(
    "possessio",
    Base.metadata,
    Column("dni_usuari", String, ForeignKey("client.dni"), primary_key=True),
    Column("matricula_cotxe", String, ForeignKey("cotxe.matricula"), primary_key=True),
)

class Robot(Base):
    __tablename__ = "robot"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    identificador = Column(String, unique=True, index=True)
    ip = Column(String)
    estat = Column(String)  # "online" o "offline"
    ultima_connexio = Column(DateTime, default=datetime.utcnow)


class Usuari(Base):
    __tablename__ = "usuari"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    data_naixement = Column(Date, nullable=False)
    ciutat = Column(String, nullable=False)
    pais = Column(String, nullable=True)
    password = Column(String, nullable=False)

    client = relationship("Client", back_populates="usuari", uselist=False)
    policia = relationship("Policia", back_populates="usuari", uselist=False)


class Client(Base):
    __tablename__ = "client"
    dni = Column(String, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("usuari.id", ondelete="CASCADE"), nullable=False)
    nom = Column(String, nullable=False)
    cognoms = Column(String, nullable=True)
    direccio = Column(String, nullable=True)
    codi_postal = Column(String, nullable=True)
    telefon = Column(String, nullable=True)

    usuari = relationship("Usuari", back_populates="client")
    cotxes = relationship("Cotxe", secondary=possessio_table, back_populates="clients")
    #targetes = relationship("ClientTargeta", back_populates="client")
    estades = relationship("Estada", back_populates="client")


class Policia(Base):
    __tablename__ = "policia"
    user_id = Column(Integer, ForeignKey("usuari.id", ondelete="CASCADE"), primary_key=True)
    placa = Column(String, unique=True, nullable=False)

    usuari = relationship("Usuari", back_populates="policia")


class Cotxe(Base):
    __tablename__ = "cotxe"
    matricula = Column(String, primary_key=True)
    marca = Column(String)
    model = Column(String)
    color = Column(String)
    any_matriculacio = Column(Integer)
    imatge = Column(String)
    dgt = Column(String)
    combustible = Column(String)

    clients = relationship("Client", secondary=possessio_table, back_populates="cotxes")
    estades = relationship("Estada", back_populates="cotxe")


class Zona(Base):
    __tablename__ = "zona"
    id = Column(Integer, primary_key=True, index=True)
    tipus = Column(String)
    ciutat = Column(String)
    carrer = Column(String)
    preu_min = Column(DECIMAL)
    temps_maxim = Column(Integer)
    coordenades = Column(String)

    estades = relationship("Estada", back_populates="zona")


class Estada(Base):
    __tablename__ = "estada"
    id = Column(Integer, primary_key=True, index=True)
    dni_usuari = Column(String, ForeignKey("client.dni"))
    matricula_cotxe = Column(String, ForeignKey("cotxe.matricula"))
    id_zona = Column(Integer, ForeignKey("zona.id"))
    data_inici = Column(TIMESTAMP)
    data_final = Column(TIMESTAMP)
    durada = Column(Interval)
    preu = Column(DECIMAL)
    activa = Column(Boolean)

    client = relationship("Client", back_populates="estades")
    cotxe = relationship("Cotxe", back_populates="estades")
    zona = relationship("Zona", back_populates="estades")

class Infraccio(Base):
    __tablename__ = "infraccio"
    id = Column(Integer, primary_key=True, index=True)
    dni_usuari = Column(String, ForeignKey("client.dni"))
    matricula_cotxe = Column(String, ForeignKey("cotxe.matricula"))
    id_zona = Column(Integer, ForeignKey("zona.id"))
    data_infraccio = Column(TIMESTAMP)
    descripcio = Column(String)
    preu = Column(DECIMAL)
    imatge = Column(String)

    # Relacions (opcionals)
    client = relationship("Client", backref="infraccions")
    cotxe = relationship("Cotxe", backref="infraccions")
    zona = relationship("Zona", backref="infraccions")


class PossibleInfraccio(Base):
    __tablename__ = "possibleinfraccio"
    id = Column(String, primary_key=True, index=True)
    descripcio = Column(String)
    matricula_cotxe = Column(String, ForeignKey("cotxe.matricula"))
    data_posinfraccio = Column(TIMESTAMP)
    imatge = Column(String)

    cotxe = relationship("Cotxe", backref="possibles_infraccions")


class Ruta(Base):
    __tablename__ = "ruta"
    id = Column(Integer, primary_key=True, index=True)
    id_policia = Column(Integer, ForeignKey("policia.user_id"))
    id_zona = Column(Integer, ForeignKey("zona.id"))
    data_creacio = Column(TIMESTAMP, nullable=False)
    origen = Column(String, nullable=False)
    desti = Column(String, nullable=False)

    policia = relationship("Policia", backref="rutes")
    zona = relationship("Zona", backref="rutes")
    punts = relationship("PuntRuta", back_populates="ruta", cascade="all, delete-orphan")
    robocats_assignats = relationship("RoboCatRuta", back_populates="ruta")


class PuntRuta(Base):
    __tablename__ = "puntruta"
    id = Column(Integer, primary_key=True, index=True)
    id_ruta = Column(Integer, ForeignKey("ruta.id"))
    latitud = Column(DECIMAL(9, 6), nullable=False)
    longitud = Column(DECIMAL(9, 6), nullable=False)
    ordre = Column(Integer, nullable=False)

    ruta = relationship("Ruta", back_populates="punts")


class RoboCatRuta(Base):
    __tablename__ = "robocatruta"
    id = Column(Integer, primary_key=True, index=True)
    id_robocat = Column(Integer, ForeignKey("robot.id"))
    id_ruta = Column(Integer, ForeignKey("ruta.id"))
    data_inici = Column(TIMESTAMP)
    data_fi = Column(TIMESTAMP)

    robocat = relationship("Robot", backref="assignacions")
    ruta = relationship("Ruta", back_populates="robocats_assignats")
