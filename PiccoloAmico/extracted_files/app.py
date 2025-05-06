from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'allevamento.db'

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
    conn = get_db_connection()
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
    conn.close()
    return render_template('dettaglio.html', cane=cane, eventi=eventi)

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



@app.route('/backup')
def backup():
    if os.path.exists('allevamento.db'):
        shutil.copyfile('allevamento.db', 'allevamento.db.bak')
        return 'Backup eseguito: allevamento.db.bak'
    return 'Database non trovato'

@app.route('/pdf/<int:id>')
def genera_pdf(id):
    from flask import make_response
    import pdfkit
    conn = get_db_connection()
    cane = conn.execute('SELECT * FROM cani WHERE id = ?', (id,)).fetchone()
    eventi = conn.execute('SELECT * FROM eventi WHERE cane_id = ? ORDER BY data DESC', (id,)).fetchall()
    conn.close()
    html = render_template('pdf_cane.html', cane=cane, eventi=eventi)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=cane_{id}.pdf'
    return response

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    totale = conn.execute('SELECT COUNT(*) FROM cani').fetchone()[0]
    in_calore = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%calore%'").fetchone()[0]
    incinte = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%incinta%'").fetchone()[0]
    fuori = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%fuori%'").fetchone()[0]
    conn.close()
    return render_template('dashboard.html', totale=totale, in_calore=in_calore, incinte=incinte, fuori=fuori)



from flask import jsonify

@app.route('/api/dashboard')
def api_dashboard():
    conn = get_db_connection()
    totale = conn.execute('SELECT COUNT(*) FROM cani').fetchone()[0]
    in_calore = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%calore%'").fetchone()[0]
    incinte = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%incinta%'").fetchone()[0]
    fuori = conn.execute("SELECT COUNT(*) FROM cani WHERE stato LIKE '%fuori%'").fetchone()[0]
    conn.close()
    return jsonify({
        'totale': totale,
        'in_calore': in_calore,
        'incinte': incinte,
        'fuori': fuori
    })


if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
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
        conn.commit()
        conn.close()
    app.run(debug=True, host='0.0.0.0')
