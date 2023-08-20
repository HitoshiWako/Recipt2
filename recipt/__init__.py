import os

from flask import Blueprint,Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db',
        UPLOAD_FOLDER='images'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # set SQLalchemy 
    db.init_app(app)
    Migrate(app, db)

    # register Blueprint
    img_app = Blueprint("images", __name__, static_url_path='/images', static_folder=os.path.join(app.instance_path,app.config['UPLOAD_FOLDER']))
    app.register_blueprint(img_app)

    from . import recipt
    app.register_blueprint(recipt.bp)
    
    from . import store
    app.register_blueprint(store.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app