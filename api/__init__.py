import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.exceptions import HTTPException

from .exceptions import handle_exception, handle_http_exception

__version__ = (0, 0, 1, "dev")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # enable CORS
    CORS(
        app,
        origins=["*", "http://localhost:*", "http://127.0.0.1:*"],
        intercept_exceptions=True,
    )

    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        db_url = "mysql+pymysql://user:password@localhost/water_quality"

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_url,
    )

    if test_config:
        # load the test config if passed in
        app.logger.debug("Loading test config")
        app.config.update(test_config)

    # initialize Flask-SQLAlchemy
    db.init_app(app)

    # Import here to prevent circular imports
    from .blueprints import records

    app.register_blueprint(records.bp)

    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_exception)

    return app
