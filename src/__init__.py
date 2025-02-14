"""
Flask main module
"""

from flask import Flask, Response

from src.config import Config
from src.core.views import core_bp
from src.errors.handlers import error_bp
from src.posts.views import post_bp
from src.webhooks.views import webhook_bp


def create_app() -> Flask:
    """
    App factory that instantiates Flask and
    returns an application object

    Returns:
        Flask: Flask app instance
    """
    application = Flask(__name__)
    app_config = Config()
    application.config.from_object(app_config)

    # register blueprints
    application.register_blueprint(core_bp)
    application.register_blueprint(error_bp)
    application.register_blueprint(post_bp)
    application.register_blueprint(webhook_bp)

    # additional security headers in responses
    @application.after_request
    def _(response: Response) -> Response:
        """
        Sets additional secure HTTP headers in request
        responses

        Args:
            response (Response): HTTP response
        Returns:
            Response: The response to a request
        """
        default = "default-src 'self'; "
        script = "script-src 'self' 'unsafe-inline'; "
        style = "style-src 'self' 'unsafe-inline';"
        connect = "connect-src 'self' https://app.greenweb.org; "
        img = "img-src data: https: 'self' https://app.greenweb.org; "
        response.headers['Content-Security-Policy'] = default + \
            script + style + connect + img
        response.headers['X-XSS-Protection'] = "1; mode=block"
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response

    return application
