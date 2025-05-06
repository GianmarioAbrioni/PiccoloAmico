#!/usr/bin/env bash
# Exit on error
set -o errexit

# Nota: Render non permette comandi apt-get da build.sh 
# wkhtmltopdf e xvfb devono già essere installati nell'immagine di base di Render
# Vedi: https://render.com/docs/create-a-dockerfile

# Installa le dipendenze Python
python -m pip install --upgrade pip
pip install -r requirements.txt

# Crea le tabelle del database se non esistono
python -c "from main import app; from models import db; with app.app_context(): db.create_all()"

# Esegui lo script di inizializzazione database che verifica tutte le tabelle e colonne
python init_database.py