"""
GitHub Webhook endpoints 
"""

import hmac
import hashlib
import subprocess
import os

from flask import abort, Blueprint, Response, request

webhook_bp = Blueprint(
    "webhooks",
    __name__,
)

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")


def verify_signature(payload_body: dict, signature: str) -> bool:
    """
    Verifies the signature of the payload body

    Args:
        payload_body (dict): request payload
        signature (str): request signature

    Returns:
        bool: True if the signature is valid
    """
    if GITHUB_WEBHOOK_SECRET is None:
        # skip verification if no secret is set
        return True

    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        payload_body,
        hashlib.sha256
    )
    return hmac.compare_digest("sha256=" + mac.hexdigest(), signature)


@webhook_bp.route("/update_webhook/", methods=["POST"])
def update_webhook() -> Response:
    """
    Triggers a deployment when a commit message contains
    the keyword '[update]'

    Returns:
        Response: HTTP response 
    """
    signature = request.headers.get("X-Hub-Signature-256")
    if not verify_signature(request.data, signature):
        # invalid signature
        abort(403)

    payload = request.json
    commits = payload.get("commits", [])

    # Check commit messages
    for commit in commits:
        if "[update]" in commit.get("message", ""):
            subprocess.run(
                [
                    "/bin/bash",
                    "/home/your-username/your-project/scripts/update.sh"
                ],
                check=False
            )
            return "Update triggered", 200

    return "Update keyword not found", 200
