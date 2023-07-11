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
    db_notes = db.execute('SELECT * FROM notes').fetchall()
    notes = []
    for note in db_notes:
        notes.append(markdown(note['content']))
    return render_template('notes/index.html', notes=notes)