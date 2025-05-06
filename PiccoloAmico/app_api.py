from datetime import datetime

def calcola_eta(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        oggi = datetime.today()
        anni = oggi.year - data.year - ((oggi.month, oggi.day) < (data.month, data.day))
        mesi = (oggi.month - data.month) % 12
        return f"{anni} anni, {mesi} mesi"
    except:
        return "-"

from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import sqlite3
import os
import shutil
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key-for-security')
CORS(app)
DB_NAME = 'allevamento.db'

# Function to verify and initialize database tables
def verify_database_tables():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS vaccinazioni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cane_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                data DATE NOT NULL,
                note TEXT,
                FOREIGN KEY (cane_id) REFERENCES cani (id)
            )
        ''')
        conn.commit()
        conn.close()
        conn = sqlite3.connect(DB_NAME)
        conn.execute('''
            CREATE TABLE cani (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                razza TEXT,
                colore TEXT,
                microchip TEXT,
                box TEXT,
                stato TEXT DEFAULT ''
            )
        ''')
        conn.execute('''
            CREATE TABLE eventi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cane_id INTEGER,
                tipo TEXT,
                descrizione TEXT,
                data TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE mating_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dog_id INTEGER,
                date TEXT,
                type TEXT,
                FOREIGN KEY (dog_id) REFERENCES cani (id)
            )
        ''')
        conn.execute('''
            CREATE TABLE births (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dog_id INTEGER,
                date TEXT,
                puppies_count INTEGER,
                type TEXT,
                FOREIGN KEY (dog_id) REFERENCES cani (id)
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized with required tables.")
    else:
        # Ensure tables exist even if file exists but is empty
        conn = sqlite3.connect(DB_NAME)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cani (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                razza TEXT,
                colore TEXT,
                microchip TEXT,
                box TEXT,
                stato TEXT DEFAULT ''
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS eventi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cane_id INTEGER,
                tipo TEXT,
                descrizione TEXT,
                data TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS mating_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dog_id INTEGER,
                date TEXT,
                type TEXT,
                FOREIGN KEY (dog_id) REFERENCES cani (id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS births (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dog_id INTEGER,
                date TEXT,
                puppies_count INTEGER,
                type TEXT,
                FOREIGN KEY (dog_id) REFERENCES cani (id)
            )
        ''')
        conn.commit()
        conn.close()
        print("Verified database tables exist.")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    totale = conn.execute('SELECT COUNT(*) FROM cani').fetchone()[0]
    per_stato = conn.execute('SELECT stato, COUNT(*) as conta FROM cani GROUP BY stato').fetchall()
    per_box = conn.execute('SELECT box, COUNT(*) as conta FROM cani GROUP BY box').fetchall()
    cani = conn.execute('SELECT * FROM cani').fetchall()
    conn.close()
    return render_template('index.html', cani=cani, totale=totale, per_stato=per_stato, per_box=per_box)

@app.route('/box/<box>')
def visualizza_box(box):
    conn = get_db_connection()
    cani = conn.execute('SELECT * FROM cani WHERE box = ?', (box,)).fetchall()
    conn.close()
    return render_template('box.html', cani=cani, box=box)

@app.route('/cane/<int:id>')
def dettaglio_cane(id):
    conn = get_db_connection()
    cane = conn.execute('SELECT * FROM cani WHERE id = ?', (id,)).fetchone()
    eventi = conn.execute('SELECT * FROM eventi WHERE cane_id = ? ORDER BY data DESC', (id,)).fetchall()
    mating_events = conn.execute('SELECT * FROM mating_events WHERE dog_id = ? ORDER BY date DESC', (id,)).fetchall()
    births = conn.execute('SELECT * FROM births WHERE dog_id = ? ORDER BY date DESC', (id,)).fetchall()
    conn.close()
    return render_template('dettaglio.html', cane=cane, eventi=eventi, mating_events=mating_events, births=births)

@app.route('/aggiorna_stato/<int:id>', methods=['POST'])
def aggiorna_stato(id):
    stato = request.form['stato']
    data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    conn.execute('UPDATE cani SET stato = ? WHERE id = ?', (stato, id))
    conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)', 
                 (id, 'Stato aggiornato', stato, data_evento))
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=id))

@app.route('/sposta/<int:id>', methods=['POST'])
def sposta_cane(id):
    nuovo_box = request.form['nuovo_box']
    data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    conn.execute('UPDATE cani SET box = ? WHERE id = ?', (nuovo_box, id))
    conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                 (id, 'Spostamento box', f'Spostato in {nuovo_box}', data_evento))
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=id))

@app.route('/aggiungi', methods=('GET', 'POST'))
def aggiungi():
    if request.method == 'POST':
        nome = request.form['nome']
        razza = request.form['razza']
        colore = request.form['colore']
        microchip = request.form['microchip']
        box = request.form['box']

        conn = get_db_connection()
        conn.execute('INSERT INTO cani (nome, razza, colore, microchip, box) VALUES (?, ?, ?, ?, ?)',
                     (nome, razza, colore, microchip, box))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('aggiungi.html')

@app.route('/cani/<int:cane_id>/vaccinations', methods=['POST'])
def add_vaccination(cane_id):
    tipo = request.form['tipo']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    note = request.form.get('note', '')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO vaccinazioni (cane_id, tipo, data, note) VALUES (?, ?, ?, ?)',
                (cane_id, tipo, data, note))
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=cane_id))

@app.route('/vaccinations/<int:vacc_id>/delete', methods=['POST'])
def delete_vaccination(vacc_id):
    conn = get_db_connection()
    vac = conn.execute('SELECT cane_id FROM vaccinazioni WHERE id = ?', (vacc_id,)).fetchone()
    dog_id = vac['cane_id'] if vac else None
    
    conn.execute('DELETE FROM vaccinazioni WHERE id = ?', (vacc_id,))
    conn.commit()
    conn.close()
    
    if dog_id:
        return redirect(url_for('dettaglio_cane', id=dog_id))
    return redirect(url_for('index'))

@app.route('/modifica_cane/<int:id>', methods=('GET', 'POST'))
def modifica_cane(id):
    conn = get_db_connection()
    cane = conn.execute('SELECT * FROM cani WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if cane is None:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        nome = request.form['nome']
        razza = request.form['razza']
        colore = request.form['colore']
        box = request.form['box']
        microchip_number = request.form.get('microchip_number', '')
        microchip_date = request.form.get('microchip_date')
        birth_date = request.form.get('birth_date')
        is_sold = request.form.get('is_sold') == '1'
        microchip_inserted = request.form.get('microchip_inserted') == '1'
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE cani 
            SET nome = ?, razza = ?, colore = ?, microchip = ?, box = ?,
                microchip_date = ?, birth_date = ?
            WHERE id = ?''',
            (nome, razza, colore, microchip_number, box, 
             microchip_date, birth_date, id))
        
        # Log the modification as an event
        data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                     (id, 'Modifica dati', 'Dati del cane aggiornati', data_evento))
        
        conn.commit()
        conn.close()
        return redirect(url_for('dettaglio_cane', id=id))
        
    return render_template('modifica_cane.html', cane=cane)
    
@app.route('/elimina_cane/<int:id>', methods=['POST'])
def elimina_cane(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cani WHERE id = ?', (id,))
    conn.execute('DELETE FROM eventi WHERE cane_id = ?', (id,))
    conn.execute('DELETE FROM mating_events WHERE dog_id = ?', (id,))
    conn.execute('DELETE FROM births WHERE dog_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/cerca', methods=['GET'])
def cerca():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cani = conn.execute("SELECT * FROM cani WHERE nome LIKE ? OR microchip LIKE ?", 
                        ('%' + query + '%', '%' + query + '%')).fetchall()
    conn.close()
    return render_template('cerca.html', cani=cani, query=query)



@app.route('/filtri', methods=['GET'])
def filtri():
    stato = request.args.get('stato', '')
    box = request.args.get('box', '')
    fuori = request.args.get('fuori', '')

    query = "SELECT * FROM cani WHERE 1=1"
    params = []

    if stato:
        query += " AND stato LIKE ?"
        params.append('%' + stato + '%')

    if box:
        query += " AND box = ?"
        params.append(box)

    if fuori == 'si':
        query += " AND stato LIKE ?"
        params.append('%fuori%')
    elif fuori == 'no':
        query += " AND stato NOT LIKE ?"
        params.append('%fuori%')

    conn = get_db_connection()
    cani = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('filtri.html', cani=cani, stato=stato, box=box, fuori=fuori)



@app.route('/esporta_eventi')
def esporta_eventi():
    import pandas as pd
    conn = get_db_connection()
    eventi = conn.execute('SELECT * FROM eventi').fetchall()
    conn.close()
    df = pd.DataFrame(eventi, columns=eventi[0].keys() if eventi else [])
    file_path = 'eventi_export.xlsx'
    df.to_excel(file_path, index=False)
    return 'File esportato come eventi_export.xlsx'

@app.route('/eventi_per_data')
def eventi_per_data():
    data_min = request.args.get('dal', '')
    data_max = request.args.get('al', '')
    query = "SELECT * FROM eventi WHERE 1=1"
    params = []

    if data_min:
        query += " AND data >= ?"
        params.append(data_min)
    if data_max:
        query += " AND data <= ?"
        params.append(data_max)

    conn = get_db_connection()
    eventi = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('eventi_date.html', eventi=eventi, data_min=data_min, data_max=data_max)



@app.route('/aggiorna_presenza/<int:id>', methods=['POST'])
def aggiorna_presenza(id):
    is_out = 'is_out' in request.form
    out_date = request.form.get('out_date')
    return_date = request.form.get('return_date')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE cani 
        SET is_out = ?, out_date = ?, return_date = ? 
        WHERE id = ?''', 
        (is_out, out_date, return_date, id))
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=id))

@app.route('/backup')
def backup():
    if os.path.exists('allevamento.db'):
        shutil.copyfile('allevamento.db', 'allevamento.db.bak')
        return 'Backup eseguito: allevamento.db.bak'
    return 'Database non trovato'

@app.route('/pdf/<int:id>')
def genera_pdf(id):
    try:
        from flask import make_response
        import pdfkit
        from datetime import datetime
        conn = get_db_connection()
        cane = conn.execute('SELECT * FROM cani WHERE id = ?', (id,)).fetchone()
        eventi = conn.execute('SELECT * FROM eventi WHERE cane_id = ? ORDER BY data DESC', (id,)).fetchall()
        conn.close()
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        html = render_template('pdf_cane.html', cane=cane, eventi=eventi, now=now)
        pdf = pdfkit.from_string(html, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=cane_{id}.pdf'
        return response
    except ImportError:
        return "pdfkit library not installed - PDF generation not available"

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    totale = conn.execute('SELECT COUNT(*) FROM cani').fetchone()[0]
    in_calore = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%calore%'").fetchone()[0]
    incinte = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%incinta%'").fetchone()[0]
    fuori = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%fuori%'").fetchone()[0]
    
    # Get statistics for mating events
    mating_natural = conn.execute("SELECT COUNT(*) FROM mating_events WHERE type = 'natural'").fetchone()[0]
    mating_artificial = conn.execute("SELECT COUNT(*) FROM mating_events WHERE type = 'artificial'").fetchone()[0]
    
    # Get statistics for birth events
    birth_natural = conn.execute("SELECT COUNT(*) FROM births WHERE type = 'natural'").fetchone()[0]
    birth_cesarean = conn.execute("SELECT COUNT(*) FROM births WHERE type = 'cesarean'").fetchone()[0]
    
    # Calculate average puppies per birth
    avg_puppies = conn.execute("SELECT AVG(puppies_count) FROM births").fetchone()[0] or 0
    
    conn.close()
    return render_template('dashboard.html', totale=totale, in_calore=in_calore, incinte=incinte, fuori=fuori,
                          mating_natural=mating_natural, mating_artificial=mating_artificial,
                          birth_natural=birth_natural, birth_cesarean=birth_cesarean, avg_puppies=avg_puppies)



@app.route('/api/dashboard')
def api_dashboard():
    conn = get_db_connection()
    totale = conn.execute('SELECT COUNT(*) FROM cani').fetchone()[0]
    in_calore = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%calore%'").fetchone()[0]
    incinte = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%incinta%'").fetchone()[0]
    fuori = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%fuori%'").fetchone()[0]
    
    # Get statistics for mating events
    mating_natural = conn.execute("SELECT COUNT(*) FROM mating_events WHERE type = 'natural'").fetchone()[0]
    mating_artificial = conn.execute("SELECT COUNT(*) FROM mating_events WHERE type = 'artificial'").fetchone()[0]
    
    # Get statistics for birth events
    birth_natural = conn.execute("SELECT COUNT(*) FROM births WHERE type = 'natural'").fetchone()[0]
    birth_cesarean = conn.execute("SELECT COUNT(*) FROM births WHERE type = 'cesarean'").fetchone()[0]
    
    # Calculate average puppies per birth
    avg_puppies = conn.execute("SELECT AVG(puppies_count) FROM births").fetchone()[0] or 0
    
    conn.close()
    return jsonify({
        'totale': totale,
        'in_calore': in_calore,
        'incinte': incinte,
        'fuori': fuori,
        'mating_natural': mating_natural,
        'mating_artificial': mating_artificial,
        'birth_natural': birth_natural,
        'birth_cesarean': birth_cesarean,
        'avg_puppies': avg_puppies
    })

# Mating events routes
@app.route('/aggiungi_accoppiamento/<int:dog_id>', methods=['POST'])
def aggiungi_accoppiamento(dog_id):
    date = request.form['date']
    type = request.form['type']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO mating_events (dog_id, date, type) VALUES (?, ?, ?)',
                 (dog_id, date, type))
    
    # Log the mating event in the general events table too
    data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                 (dog_id, 'Accoppiamento', f'Tipo: {type}, Data: {date}', data_evento))
    
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=dog_id))

@app.route('/modifica_accoppiamento/<int:id>', methods=['POST'])
def modifica_accoppiamento(id):
    date = request.form['date']
    type = request.form['type']
    dog_id = request.form['dog_id']
    
    conn = get_db_connection()
    conn.execute('UPDATE mating_events SET date = ?, type = ? WHERE id = ?',
                 (date, type, id))
                 
    # Log the update in the events table
    data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                 (dog_id, 'Modifica accoppiamento', f'Aggiornato accoppiamento del {date}', data_evento))
    
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=dog_id))

@app.route('/elimina_accoppiamento/<int:id>', methods=['POST'])
def elimina_accoppiamento(id):
    conn = get_db_connection()
    mating = conn.execute('SELECT dog_id FROM mating_events WHERE id = ?', (id,)).fetchone()
    dog_id = mating['dog_id'] if mating else 0
    
    conn.execute('DELETE FROM mating_events WHERE id = ?', (id,))
    
    # Log the deletion in the events table
    if dog_id > 0:
        data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                     (dog_id, 'Eliminazione accoppiamento', 'Accoppiamento eliminato', data_evento))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('dettaglio_cane', id=dog_id) if dog_id > 0 else url_for('index'))

# Birth events routes
@app.route('/aggiungi_parto/<int:dog_id>', methods=['POST'])
def aggiungi_parto(dog_id):
    date = request.form['date']
    type = request.form['type']
    puppies_count = request.form['puppies_count']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO births (dog_id, date, type, puppies_count) VALUES (?, ?, ?, ?)',
                 (dog_id, date, type, puppies_count))
    
    # Log the birth event in the general events table too
    data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                 (dog_id, 'Parto', f'Tipo: {type}, Data: {date}, Cuccioli: {puppies_count}', data_evento))
    
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=dog_id))

@app.route('/modifica_parto/<int:id>', methods=['POST'])
def modifica_parto(id):
    date = request.form['date']
    type = request.form['type']
    puppies_count = request.form['puppies_count']
    dog_id = request.form['dog_id']
    
    conn = get_db_connection()
    conn.execute('UPDATE births SET date = ?, type = ?, puppies_count = ? WHERE id = ?',
                 (date, type, puppies_count, id))
                 
    # Log the update in the events table
    data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                 (dog_id, 'Modifica parto', f'Aggiornato parto del {date}', data_evento))
    
    conn.commit()
    conn.close()
    return redirect(url_for('dettaglio_cane', id=dog_id))

@app.route('/elimina_parto/<int:id>', methods=['POST'])
def elimina_parto(id):
    conn = get_db_connection()
    birth = conn.execute('SELECT dog_id FROM births WHERE id = ?', (id,)).fetchone()
    dog_id = birth['dog_id'] if birth else 0
    
    conn.execute('DELETE FROM births WHERE id = ?', (id,))
    
    # Log the deletion in the events table
    if dog_id > 0:
        data_evento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO eventi (cane_id, tipo, descrizione, data) VALUES (?, ?, ?, ?)',
                     (dog_id, 'Eliminazione parto', 'Parto eliminato', data_evento))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('dettaglio_cane', id=dog_id) if dog_id > 0 else url_for('index'))


# Initialize database when starting the app
verify_database_tables()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route("/cani/<int:cane_id>/aggiungi_vaccinazione", methods=["POST"])
def aggiungi_vaccinazione(cane_id):
    conn = get_db_connection()
    tipo = request.form["tipo"]
    data = request.form["data"]
    note = request.form.get("note", "")
    conn.execute("INSERT INTO vaccinazioni (cane_id, tipo, data, note) VALUES (?, ?, ?, ?)", (cane_id, tipo, data, note))
    conn.commit()
    conn.close()
    return redirect(url_for("dog_detail", dog_id=cane_id))
