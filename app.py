from pathlib import Path
import sqlite3
from flask import Flask, abort, flash, redirect, render_template, request, url_for

BASE = Path(__file__).resolve().parent
DB = BASE / 'jmatch.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'solo-desarrollo-local-cambiar-antes-de-publicar'


def connection():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def initialize():
    with connection() as db:
        db.executescript((BASE / 'schema.sql').read_text(encoding='utf-8'))


def options(db):
    categories = db.execute('SELECT * FROM categorias ORDER BY nombre').fetchall()
    features = db.execute('SELECT * FROM caracteristicas ORDER BY nombre').fetchall()
    return categories, features


def validate(form, db):
    errors = []
    nombre = form.get('nombre', '').strip()
    modelo = form.get('modelo', '').strip()
    if not nombre or not modelo:
        errors.append('Nombre y modelo son obligatorios.')
    try:
        precio = int(form.get('precio', ''))
        if precio < 0: raise ValueError()
    except ValueError:
        precio = 0
        errors.append('El precio debe ser un entero mayor o igual a cero (COP).')
    raw_size = form.get('tamano_mm', '').strip()
    try:
        tamano = int(raw_size) if raw_size else None
        if tamano is not None and tamano <= 0: raise ValueError()
    except ValueError:
        tamano = None
        errors.append('El tamaño debe ser un número entero positivo.')
    try:
        categoria = int(form.get('id_categoria', ''))
        if not db.execute('SELECT 1 FROM categorias WHERE id_categoria=?', (categoria,)).fetchone():
            raise ValueError()
    except ValueError:
        categoria = None
        errors.append('Selecciona una categoría válida.')
    selected = set()
    for raw in form.getlist('caracteristicas'):
        try: selected.add(int(raw))
        except ValueError: errors.append('Característica no válida.')
    valid = {r['id_caracteristica'] for r in db.execute('SELECT id_caracteristica FROM caracteristicas')}
    if not selected.issubset(valid): errors.append('Una característica seleccionada no existe.')
    data = (categoria, nombre, modelo, precio, tamano,
            form.get('tipo_pantalla', '').strip(),
            form.get('compatibilidad', '').strip(),
            form.get('descripcion', '').strip())
    return data, selected, errors


@app.route('/')
def index():
    with connection() as db:
        rows = db.execute('''SELECT s.*, c.nombre AS categoria,
            (SELECT GROUP_CONCAT(f.nombre, ', ') FROM smartwatch_caracteristicas sc
             JOIN caracteristicas f ON f.id_caracteristica=sc.id_caracteristica
             WHERE sc.id_smartwatch=s.id_smartwatch) AS funciones
            FROM smartwatches s JOIN categorias c ON c.id_categoria=s.id_categoria
            ORDER BY s.id_smartwatch DESC''').fetchall()
    return render_template('index.html', items=rows)


@app.route('/nuevo', methods=['GET', 'POST'])
def new():
    with connection() as db:
        cats, feats = options(db)
        if request.method == 'POST':
            data, selected, errors = validate(request.form, db)
            if errors:
                for err in errors: flash(err, 'error')
            else:
                cursor = db.execute('''INSERT INTO smartwatches
                    (id_categoria,nombre,modelo,precio,tamano_mm,tipo_pantalla,compatibilidad,descripcion)
                    VALUES (?,?,?,?,?,?,?,?)''', data)
                db.executemany('INSERT INTO smartwatch_caracteristicas VALUES (?,?)',
                               [(cursor.lastrowid, fid) for fid in selected])
                db.commit()
                flash('Smartwatch registrado correctamente.', 'success')
                return redirect(url_for('index'))
    return render_template('form.html', item=None, categories=cats, features=feats,
                           selected=set(), title='Registrar smartwatch')


@app.route('/editar/<int:watch_id>', methods=['GET', 'POST'])
def edit(watch_id):
    with connection() as db:
        item = db.execute('SELECT * FROM smartwatches WHERE id_smartwatch=?', (watch_id,)).fetchone()
        if item is None: abort(404)
        cats, feats = options(db)
        selected = {r['id_caracteristica'] for r in db.execute(
            'SELECT id_caracteristica FROM smartwatch_caracteristicas WHERE id_smartwatch=?', (watch_id,))}
        if request.method == 'POST':
            data, selected, errors = validate(request.form, db)
            if errors:
                for err in errors: flash(err, 'error')
            else:
                db.execute('''UPDATE smartwatches SET id_categoria=?, nombre=?, modelo=?,
                    precio=?, tamano_mm=?, tipo_pantalla=?, compatibilidad=?, descripcion=?
                    WHERE id_smartwatch=?''', (*data, watch_id))
                db.execute('DELETE FROM smartwatch_caracteristicas WHERE id_smartwatch=?', (watch_id,))
                db.executemany('INSERT INTO smartwatch_caracteristicas VALUES (?,?)',
                               [(watch_id, fid) for fid in selected])
                db.commit()
                flash('Smartwatch actualizado correctamente.', 'success')
                return redirect(url_for('index'))
    return render_template('form.html', item=item, categories=cats, features=feats,
                           selected=selected, title='Editar smartwatch')


@app.route('/eliminar/<int:watch_id>', methods=['POST'])
def delete(watch_id):
    with connection() as db:
        result = db.execute('DELETE FROM smartwatches WHERE id_smartwatch=?', (watch_id,))
        db.commit()
    if result.rowcount == 0: abort(404)
    flash('Smartwatch eliminado correctamente.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    initialize()
    app.run(debug=True, host='127.0.0.1', port=5000)
