import sqlite3

import click
from flask import current_app, g


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
    app.cli.add_command(add_note_command)
    app.cli.add_command(get_content_command)

def add_note(md_file):
    db = get_db()
    with open(md_file, encoding='utf8') as f:
        db.execute("INSERT INTO notes (content) VALUES (?)", (f.read(), ))
        db.commit()

def get_content():
    db = get_db()
    data = db.execute('SELECT * FROM notes').fetchall()
    return data

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


@click.command('add_note')
@click.argument('md_file')
def add_note_command(md_file):
    add_note(md_file)
    click.echo('Note is added.')

@click.command('get_content')
def get_content_command():
    click.echo(get_content())
