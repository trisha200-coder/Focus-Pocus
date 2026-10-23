import os
import requests

API_URL = os.getenv(
    "FOCUS_POCUS_API_URL",
    "http://localhost:3000"
).rstrip("/")


class DatabaseAPIError(Exception):
    """Raised when the database API request fails."""


def _request(method, path, **kwargs):
    try:
        response = requests.request(
            method,
            f"{API_URL}{path}",
            timeout=15,
            **kwargs,
        )
        response.raise_for_status()
        return response.json() if response.content else {}

    except requests.RequestException as error:
        message = "Could not communicate with the Focus-Pocus backend."

        if error.response is not None:
            try:
                message = error.response.json().get("error", message)
            except ValueError:
                pass

        raise DatabaseAPIError(message) from error


def get_subjects():
    """Return the current prototype user's subjects."""
    result = _request("GET", "/api/subjects")
    return result.get("subjects", [])


def add_subject(name):
    """Add a subject through the Express backend."""
    name = name.strip() if isinstance(name, str) else ""

    if not name:
        raise DatabaseAPIError("Please enter a subject name.")

    result = _request(
        "POST",
        "/api/subjects",
        json={"name": name},
    )
    return result.get("subject", {})


def delete_subject(subject_id):
    """Delete a subject through the Express backend."""
    result = _request(
        "DELETE",
        f"/api/subjects/{int(subject_id)}",
    )
    return result


def get_study_insights():
    """Ask the backend for AI observations based on study records."""
    result = _request("GET", "/api/study/insights")
    return result
