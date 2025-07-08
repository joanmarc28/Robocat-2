-- Taula Usuari
CREATE TABLE Usuari (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    data_naixement DATE NOT NULL,
    Ciutat TEXT NOT NULL,
    Pais TEXT
);

-- Taula Policia
CREATE TABLE Policia (
    user_id INTEGER PRIMARY KEY REFERENCES Usuari(id),
    Placa TEXT NOT NULL
);

-- Taula Client
CREATE TABLE Client (
    DNI TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES Usuari(id),
    Nom TEXT,
    Cognoms TEXT,
    codi_postal TEXT,
    direccio TEXT,
    Credits INTEGER DEFAULT 0,
    Telefon numeric(15),
);

-- Taula Cotxe
CREATE TABLE Cotxe (
    Matricula TEXT PRIMARY KEY,
    Marca TEXT,
    Model TEXT,
    Color TEXT,
    any_matriculacio INTEGER,
    Imatge TEXT,
    DGT TEXT,
    Combustible TEXT
);

-- Taula relació Usuari-Cotxe (Possessió)
CREATE TABLE Possessio (
    DNI_Usuari TEXT REFERENCES Client(DNI),
    Matricula_Cotxe TEXT REFERENCES Cotxe(Matricula),
    PRIMARY KEY (DNI_Usuari, Matricula_Cotxe)
);

-- Taula Zona
CREATE TABLE Zona (
    id SERIAL PRIMARY KEY,
    Tipus TEXT,
    Ciutat TEXT,
    Carrer TEXT,
    Preu_Min DECIMAL,
    Temps_Maxim INTEGER,
    Coordenades TEXT
);

-- Taula Estada
CREATE TABLE Estada (
    id SERIAL PRIMARY KEY,
    DNI_Usuari TEXT REFERENCES Client(DNI),
    Matricula_Cotxe TEXT REFERENCES Cotxe(Matricula),
    id_Zona INTEGER REFERENCES Zona(id),
    Data_Inici TIMESTAMP ,
    Data_Final TIMESTAMP ,
    Durada INTERVAL,
    Preu DECIMAL,
    Activa BOOLEAN
);

-- Taula Robot
CREATE TABLE robot (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    identificador TEXT UNIQUE,
    ip TEXT,
    estat TEXT, -- "online", "offline"
    id_ruta INTEGER REFERENCES Ruta(id),
    ultima_connexio TIMESTAMP
);

-- Taula infraccio
CREATE TABLE Infraccio (
    id SERIAL PRIMARY KEY,
    DNI_Usuari TEXT REFERENCES Client(DNI),
    Matricula_Cotxe TEXT REFERENCES Cotxe(Matricula),
    id_Zona INTEGER REFERENCES Zona(id),
    Data_Infraccio TIMESTAMP,
    Descripcio TEXT,
    Preu DECIMAL,
    Imatge TEXT
); 

-- Taula possibles infraccions
CREATE TABLE PossibleInfraccio (
    id VARCHAR(255) PRIMARY KEY,
    Descripcio TEXT,
    Matricula_Cotxe TEXT REFERENCES Cotxe(Matricula),
    data_posInfraccio TIMESTAMP,
    Imatge TEXT
);

-- Taula Ruta
CREATE TABLE Ruta (
    id SERIAL PRIMARY KEY,
    id_policia INTEGER REFERENCES Policia(user_id),
    id_zona INTEGER REFERENCES Zona(id),
    data_creacio TIMESTAMP NOT NULL,
    origen TEXT NOT NULL,
    desti TEXT NOT NULL
);

-- Taula PuntRuta (llista de punts d'una ruta)
CREATE TABLE PuntRuta (
    id SERIAL PRIMARY KEY,
    id_Ruta INTEGER REFERENCES Ruta(id),
    latitud DECIMAL(9,6) NOT NULL,
    longitud DECIMAL(9,6) NOT NULL,
    ordre INTEGER NOT NULL -- ordre del punt dins de la ruta
);

-- Taula RoboCatRuta (assignació de RoboCat a Ruta)
CREATE TABLE RoboCatRuta (
    id SERIAL PRIMARY KEY,
    id_RoboCat INTEGER REFERENCES robot(id),
    id_Ruta INTEGER REFERENCES Ruta(id),
    data_inici TIMESTAMP,
    data_fi TIMESTAMP
);
