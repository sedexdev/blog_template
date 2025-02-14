"""
Module for reloading the PythonAnywhere server
"""

import os

import requests

USERNAME = os.getenv("PYTHONANYWHERE_USERNAME")
TOKEN = os.getenv("PYTHONANYWHERE_API_TOKEN")
HOST = os.getenv("PYTHONANYWHERE_HOST")
DOMAIN = os.getenv("PYTHONANYWHERE_DOMAIN")


def reload_web_app() -> None:
    """
    Reloads the Web app after changes
    """
    requests.post(
        url=f"https://{HOST}/api/v0/user/{USERNAME}/webapps/{DOMAIN}/reload/",
        headers={"Authorization": f"Token {TOKEN}"},
        timeout=60
    )


reload_web_app()
