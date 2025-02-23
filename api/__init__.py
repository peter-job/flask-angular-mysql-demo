import os

from flask import Flask, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.exceptions import HTTPException, InternalServerError

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

    from api.blueprints import water_quality

    app.register_error_handler(
        Exception, lambda e: print("Error!!!!") & {"error": str(e)}
    )

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "message": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = InternalServerError().get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": 500,
                "name": "Internal Server Error",
                "message": "Uh oh! Something went wrong.",
            }
        )
        response.content_type = "application/json"
        return response

    app.register_blueprint(water_quality.bp)

    return app
