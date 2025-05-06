"""
Script per inizializzare il database con tutte le tabelle necessarie
"""
import sys
from main import app
from models import db, Dog, Vaccination, Mating, Birth, OutLog
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def init_database():
    """Crea tutte le tabelle se non esistono"""
    with app.app_context():
        try:
            # Crea tutte le tabelle definite nei modelli
            db.create_all()
            print("✅ Tutte le tabelle create con successo!")
            
            # Verifica l'esistenza della tabella out_logs
            result = db.session.execute(text("SELECT to_regclass('out_logs')")).scalar()
            if not result:
                print("⚠️ La tabella out_logs non esiste, creazione in corso...")
                # Crea la tabella OutLog
                OutLog.__table__.create(db.engine)
                print("✅ Tabella out_logs creata con successo!")
                
            return True
        except SQLAlchemyError as e:
            print(f"❌ Errore nella creazione delle tabelle: {str(e)}")
            return False

def verify_columns():
    """Verifica che le colonne necessarie esistano nelle tabelle"""
    with app.app_context():
        try:
            # Verifica che box, is_out, out_date e return_date esistano nella tabella dogs
            columns = db.session.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'dogs'"
            )).scalars().all()
            
            columns_set = set(columns)
            required_columns = {'box', 'is_out', 'out_date', 'return_date'}
            missing_columns = required_columns - columns_set
            
            if missing_columns:
                print(f"⚠️ Colonne mancanti nella tabella dogs: {missing_columns}")
                # Aggiungi le colonne mancanti
                for column in missing_columns:
                    if column == 'box':
                        db.session.execute(text(
                            "ALTER TABLE dogs ADD COLUMN box VARCHAR(50) DEFAULT ''"
                        ))
                    elif column == 'is_out':
                        db.session.execute(text(
                            "ALTER TABLE dogs ADD COLUMN is_out BOOLEAN DEFAULT FALSE"
                        ))
                    elif column == 'out_date':
                        db.session.execute(text(
                            "ALTER TABLE dogs ADD COLUMN out_date DATE"
                        ))
                    elif column == 'return_date':
                        db.session.execute(text(
                            "ALTER TABLE dogs ADD COLUMN return_date DATE"
                        ))
                
                db.session.commit()
                print("✅ Tutte le colonne mancanti aggiunte con successo!")
            else:
                print("✅ Tutte le colonne necessarie esistono nella tabella dogs")
            
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Errore nella verifica/aggiunta delle colonne: {str(e)}")
            return False

if __name__ == "__main__":
    print("Inizializzazione del database in corso...")
    
    # Crea tutte le tabelle
    if not init_database():
        sys.exit(1)
    
    # Verifica le colonne necessarie
    if not verify_columns():
        sys.exit(1)
    
    print("✅ Inizializzazione del database completata con successo!")