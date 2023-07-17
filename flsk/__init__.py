import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flsk.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    from . import db
    db.init_app(app)

    from . import notes, adm
    app.register_blueprint(adm.bp)
    app.register_blueprint(notes.bp)
    app.add_url_rule('/', endpoint='index')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app