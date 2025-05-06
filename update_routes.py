"""
Routes per l'aggiornamento del database
"""
from flask import flash, redirect, url_for
from app import app
from sqlalchemy import text, exc
from models import db, OutLog

@app.route('/update_database')
def update_database():
    """Aggiorna il database aggiungendo le colonne necessarie per PostgreSQL."""
    try:
        # Ottieni le colonne esistenti nella tabella dogs
        columns = []
        try:
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'dogs'
            """))
            columns = [row[0] for row in result.fetchall()]
            app.logger.info(f"Colonne esistenti: {columns}")
        except Exception as e:
            app.logger.error(f"Errore nel leggere le colonne: {str(e)}")
        
        # Aggiungi box se non esiste
        if 'box' not in columns:
            try:
                db.session.execute(text("ALTER TABLE dogs ADD COLUMN box VARCHAR(50) DEFAULT ''"))
                app.logger.info("Colonna 'box' aggiunta con successo")
            except Exception as e:
                app.logger.error(f"Errore nell'aggiunta della colonna 'box': {str(e)}")
        
        # Aggiungi is_out se non esiste
        if 'is_out' not in columns:
            try:
                db.session.execute(text("ALTER TABLE dogs ADD COLUMN is_out BOOLEAN DEFAULT FALSE"))
                app.logger.info("Colonna 'is_out' aggiunta con successo")
            except Exception as e:
                app.logger.error(f"Errore nell'aggiunta della colonna 'is_out': {str(e)}")
        
        # Aggiungi out_date se non esiste
        if 'out_date' not in columns:
            try:
                db.session.execute(text("ALTER TABLE dogs ADD COLUMN out_date DATE"))
                app.logger.info("Colonna 'out_date' aggiunta con successo")
            except Exception as e:
                app.logger.error(f"Errore nell'aggiunta della colonna 'out_date': {str(e)}")
        
        # Aggiungi return_date se non esiste
        if 'return_date' not in columns:
            try:
                db.session.execute(text("ALTER TABLE dogs ADD COLUMN return_date DATE"))
                app.logger.info("Colonna 'return_date' aggiunta con successo")
            except Exception as e:
                app.logger.error(f"Errore nell'aggiunta della colonna 'return_date': {str(e)}")
        
        # Verifica l'esistenza della tabella out_logs
        try:
            result = db.session.execute(text("""
                SELECT to_regclass('public.out_logs')
            """))
            table_exists = result.scalar() is not None
            
            if not table_exists:
                # Crea la tabella out_logs se non esiste
                db.session.execute(text("""
                    CREATE TABLE out_logs (
                        id SERIAL PRIMARY KEY,
                        dog_id INTEGER NOT NULL,
                        action VARCHAR(10) NOT NULL,
                        date DATE NOT NULL,
                        expected_return_date DATE,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (dog_id) REFERENCES dogs (id)
                    )
                """))
                app.logger.info("Tabella 'out_logs' creata con successo")
        except Exception as e:
            app.logger.error(f"Errore nella creazione della tabella 'out_logs': {str(e)}")
        
        # Commit delle modifiche
        db.session.commit()
        
        # Assicurati che tutti i modelli siano sincronizzati
        with app.app_context():
            db.create_all()
        
        flash('Database aggiornato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Errore generale: {str(e)}")
        flash(f'Errore durante l\'aggiornamento del database: {str(e)}', 'danger')
    
    return redirect(url_for('index', db_updated=True))