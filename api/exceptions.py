import json

from flask import Response, current_app
from werkzeug.exceptions import HTTPException, InternalServerError


def handle_http_exception(e: HTTPException) -> Response:
    """Return JSON instead of HTML for HTTP exceptions."""
    current_app.logger.error(f"HTTP Exception: {e.code} - {e.name} - {e.description}")
    response: Response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "message": e.description,
        }
    )
    response.content_type = "application/json"
    return response


def handle_exception(e: Exception) -> Response:
    """Return JSON instead of HTML for unexpected exceptions."""
    current_app.logger.error("Unexpected exception", exc_info=e)
    response: Response = InternalServerError().get_response()
    response.data = json.dumps(
        {
            "code": 500,
            "name": "Internal Server Error",
            "message": "Uh oh! Something went wrong.",
        }
    )
    response.content_type = "application/json"
    return response
