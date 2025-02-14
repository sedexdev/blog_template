"""
HTTP Error code response handlers
"""


from flask import Blueprint, render_template, Response
from werkzeug.exceptions import NotFound, InternalServerError

error_bp = Blueprint(
    "error",
    __name__,
    template_folder="templates"
)


@error_bp.app_errorhandler(NotFound)
def handle_not_found(e: Response) -> Response:
    """
    Handles a page not found 404 error

    Args:
        e (Response): response error object

    Returns:
        Response: response to return
    """
    return render_template("404.html", error=e.description), 404


@error_bp.app_errorhandler(InternalServerError)
def handle_internal_server_error(e: Response) -> Response:
    """
    Handles an internal server 500 error

    Args:
        e (Response): response error object

    Returns:
        Response: response to return
    """
    return render_template("500.html", error=e.description), 500
