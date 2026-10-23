"""Focus Pocus database service.

All database operations go through the Express backend.
Supabase credentials must remain on the backend.
"""

import os
import requests

API_URL = os.getenv(
    "FOCUS_POCUS_API_URL",
    "http://localhost:3000",
).rstrip("/")

TIMEOUT = 15


class DatabaseAPIError(Exception):
    """Raised when a backend request fails."""


def _request(method, path, **kwargs):
    """Send a request to the Express backend."""
    try:
        response = requests.request(
            method,
            f"{API_URL}{path}",
            timeout=TIMEOUT,
            **kwargs,
        )
        response.raise_for_status()

        if not response.content:
            return {}

        try:
            return response.json()
        except ValueError as error:
            raise DatabaseAPIError(
                "The backend returned an invalid response."
            ) from error

    except requests.RequestException as error:
        message = "Could not communicate with the Focus-Pocus backend."

        if error.response is not None:
            try:
                message = error.response.json().get("error", message)
            except (ValueError, AttributeError):
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

    if len(name) > 100:
        raise DatabaseAPIError(
            "Subject name must contain no more than 100 characters."
        )

    result = _request(
        "POST",
        "/api/subjects",
        json={"name": name},
    )
    return result.get("subject", {})


def delete_subject(subject_id):
    """Delete a subject through the Express backend."""
    try:
        subject_id = int(subject_id)
    except (TypeError, ValueError) as error:
        raise DatabaseAPIError(
            "Please provide a valid subject ID."
        ) from error

    if subject_id <= 0:
        raise DatabaseAPIError("Please provide a valid subject ID.")

    return _request("DELETE", f"/api/subjects/{subject_id}")


def get_study_sessions():
    """Fetch completed study sessions from the backend."""
    try:
        result = _request("GET", "/api/study/insights")
        return result.get("study_data", [])
    except Exception:
        return []


def check_in_session(subject_id):
    """Start a new study session."""
    return _request("POST", "/api/study/check-in", json={"subjectId": subject_id})


def check_out_session(session_id):
    """Complete an active study session."""
    return _request("POST", "/api/study/check-out", json={"sessionId": session_id})


def get_study_insights():
    """Fetch AI-generated study insights from the backend."""
    result = _request("GET", "/api/study/insights")
    return result.get("insights", result)
