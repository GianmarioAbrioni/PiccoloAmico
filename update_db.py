"""
Script per aggiornare il database, aggiungendo i campi box, is_out, out_date e return_date
alla tabella dogs.
"""
import sys
from main import app
from models import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def add_box_column():
    """Aggiunge la colonna box alla tabella dogs se non esiste già."""
    with app.app_context():
        try:
            db.session.execute(text(
                "ALTER TABLE dogs ADD COLUMN IF NOT EXISTS box VARCHAR(50) DEFAULT ''"
            ))
            db.session.commit()
            print("✅ Colonna 'box' aggiunta con successo!")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Errore nell'aggiunta della colonna 'box': {str(e)}")
            return False
    return True

def add_out_columns():
    """Aggiunge le colonne is_out, out_date e return_date alla tabella dogs se non esistono già."""
    with app.app_context():
        try:
            # Aggiungi is_out
            db.session.execute(text(
                "ALTER TABLE dogs ADD COLUMN IF NOT EXISTS is_out BOOLEAN DEFAULT FALSE"
            ))
            
            # Aggiungi out_date
            db.session.execute(text(
                "ALTER TABLE dogs ADD COLUMN IF NOT EXISTS out_date DATE"
            ))
            
            # Aggiungi return_date
            db.session.execute(text(
                "ALTER TABLE dogs ADD COLUMN IF NOT EXISTS return_date DATE"
            ))
            
            db.session.commit()
            print("✅ Colonne 'is_out', 'out_date' e 'return_date' aggiunte con successo!")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Errore nell'aggiunta delle colonne 'is_out', 'out_date' e 'return_date': {str(e)}")
            return False
    return True

if __name__ == "__main__":
    print("Aggiornamento del database in corso...")
    
    # Aggiungi colonna box
    if not add_box_column():
        sys.exit(1)
    
    # Aggiungi colonne relative allo stato "fuori struttura"
    if not add_out_columns():
        sys.exit(1)
    
    print("✅ Aggiornamento del database completato con successo!")