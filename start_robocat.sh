#!/bin/bash
set -e  # Atura el script si hi ha algun error

# Activa l'entorn virtual
source /home/Robocat/robocat_env/bin/activate

# Va al directori de l'app
cd /home/Robocat/Robocat/app

# Executa el programa principal
exec python main.py
