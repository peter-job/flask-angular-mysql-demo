import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

__version__ = (0, 0, 1, "dev")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        app.logger.debug("No DATABASE_URL found in environ, using default")
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

    from api import water_quality

    app.register_blueprint(water_quality.bp)

    return app
