import functools
from markdown import markdown
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flsk.db import get_db

bp = Blueprint('adm', __name__, url_prefix='/adm')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('adm/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('adm.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        tags = request.form['tags']
        preview = request.form['preview']
        content = request.form['content']
        db = get_db()
        error = None

        if not title:
            error = 'Title is required'
        tags = tags.lower()
        content = markdown(content)
        preview = markdown(preview)
        if error is None:
            db.execute('INSERT INTO note (title, tag, preview, content) VALUES (?, ?, ?, ?)', 
                       (title, tags, preview, content))
            db.commit()
            return redirect(url_for('index'))

        flash(error)

    return render_template('adm/add_note.html')


@bp.route('/delete/<int:id>', methods=('GET',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM note WHERE id = ?', (id, ))
    db.commit()
    return redirect(url_for('index'))