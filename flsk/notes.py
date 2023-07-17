from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from markdown import markdown
from werkzeug.exceptions import abort

from flsk.db import get_db

bp = Blueprint('notes', __name__)


@bp.route('/')
def index():
    db = get_db()
    db_notes = db.execute('SELECT * FROM note').fetchall()
    tags = db.execute('SELECT tag FROM note GROUP BY tag').fetchall()
    return render_template('notes/index.html', notes=db_notes, tags=tags)

@bp.route('/tag/<tag>')
def tag(tag):
    db = get_db()
    db_notes = db.execute("SELECT * FROM note WHERE tag LIKE ?", (f'%{tag}%', )).fetchall()
    tags = db.execute('SELECT tag FROM note GROUP BY tag').fetchall()
    return render_template('notes/index.html', notes=db_notes, tags=tags)

@bp.route('/note/<int:id>')
def note(id):
    db = get_db()
    note = db.execute("SELECT * FROM note WHERE id = ?", (id, )).fetchone()
    tags = db.execute('SELECT tag FROM note GROUP BY tag').fetchall()
    return render_template('notes/note.html', note=note, tags=tags)