import sqlite3
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_user_command)
    app.cli.add_command(get_content_command)


def add_user(username, password):
    db = get_db()
    try:
        db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)))
        db.commit()
    except db.IntegrityError:
        return 'User already registered.'
    else:
        return 'User registered.'

def get_content():
    db = get_db()
    data = db.execute('SELECT * FROM note').fetchall()
    return data

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


@click.command('add_user')
@click.argument('username')
@click.argument('password')
def add_user_command(username, password):
    result = add_user(username, password)
    click.echo(result)

@click.command('get_content')
def get_content_command():
    click.echo(get_content())
