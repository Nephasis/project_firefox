import os
import sqlite3
from flask import Flask, render_template, request, redirect, g, send_from_directory

app = Flask(__name__)
app.config.from_object(__name__)

# Config
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'database/records.db'),
    DEBUG = True,
    UPLOAD_FOLDER = 'uploads',
    OUTPUT_FOLDER = 'outputs',
    OUTPUT_NAME = 'topologia_wynik',
    SCRIPT_NAME = 'topologia.py',
    ALLOWED_EXTENSIONS = set(['txt', 'gro', 'doc', 'docx'])
    ))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def run_calculations(filename, output_id):
    script = os.path.join(app.root_path, app.config['SCRIPT_NAME'])
    in_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    out_file = os.path.join(app.config['OUTPUT_FOLDER'], app.config['OUTPUT_NAME'] + str(output_id) + '.top')
    os.spawnlp(os.P_NOWAIT, 'python', 'python', script, in_file, out_file)
    return out_file

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def check_output():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM records WHERE calculated = 0')
    rows = cur.fetchall()
    for row in rows:
        out_name = app.config['OUTPUT_NAME'] + str(row[0]) + '.top'
        output_name = os.path.join(app.config['OUTPUT_FOLDER'], out_name)
        if os.path.exists(output_name):
            cur.execute('UPDATE Records SET calculated=?, output_file=? WHERE Id=?', (1, out_name, row[0]))
        else:
            pass
    get_db().commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods = ['GET', 'POST'])
def index():
    check_output()
    db = get_db()
    cur = db.execute('SELECT * FROM records ORDER BY id DESC LIMIT(10)')
    latest_calcs = cur.fetchall()
    return render_template('index.html', calcs = latest_calcs)

@app.route('/outputs/<filename>')
def calculated_record(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/upload', methods = ['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        cur = get_db().cursor()
        cur.execute("INSERT INTO records(calculated, date, time) VALUES(0, Date('now'), Time('now'))", )
        file_id = cur.lastrowid
        get_db().commit()
        input_file = str(file_id) +'.'+file.filename.rsplit('.', 1)[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], input_file))

        output_name = run_calculations(input_file, file_id)

        if os.path.exists(output_name):
            return redirect(output_name)
        else:
            return redirect('/')
    else:
        return "Something went wrong, check if your file is in right format ('txt', 'gro', 'doc', 'docx')"

if __name__ == '__main__':
    app.run()
