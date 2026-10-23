
"""Focus Pocus database service.

All database operations go through the Express backend.
Supabase credentials must remain on the backend.
"""

import os
import requests

API_BASE_URL = os.getenv(
    "FOCUS_POCUS_API_URL",
    "http://localhost:3000"
).rstrip("/")

TIMEOUT = 15


class DatabaseAPIError(Exception):
    """Raised when a backend request fails."""
    pass


def _request(method, endpoint, payload=None):
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{endpoint}",
            json=payload,
            timeout=TIMEOUT,
        )

        try:
            data = response.json()
        except ValueError:
            data = {}

        if not response.ok:
            raise DatabaseAPIError(
                data.get("error", f"HTTP error {response.status_code}")
            )

        return data

    except requests.Timeout as exc:
        raise DatabaseAPIError("Backend request timed out.") from exc

    except requests.ConnectionError as exc:
        raise DatabaseAPIError(
            "Cannot connect to Express. Check that npm start is running."
        ) from exc

    except requests.RequestException as exc:
        raise DatabaseAPIError(f"Request failed: {exc}") from exc


# ---------------- SUBJECTS ----------------

def get_subjects():
    """Return subjects belonging to the configured prototype user."""
    return _request("GET", "/api/subjects").get("subjects", [])


def add_subject(name):
    """Insert a subject into the subjects table."""
    if not isinstance(name, str) or not name.strip():
        raise DatabaseAPIError("Enter a subject name.")

    return _request(
        "POST",
        "/api/subjects",
        {"name": name.strip()},
    ).get("subject")


# ---------------- STUDY SESSIONS ----------------

def start_study_session(subject_id):
    """Create an active session; returns its database ID."""
    return _request(
        "POST",
        "/api/study/check-in",
        {"subjectId": int(subject_id)},
    ).get("session")


def end_study_session(session_id):
    """Finish an active session and return its duration."""
    return _request(
        "POST",
        "/api/study/check-out",
        {"sessionId": int(session_id)},
    )


def complete_study_session(subject_id, minutes):
    """Save a completed timer session in one request."""
    minutes = int(minutes)

    if not 1 <= minutes <= 180:
        raise DatabaseAPIError(
            "Session duration must be between 1 and 180 minutes."
        )

    return _request(
        "POST",
        "/api/study/complete",
        {
            "subjectId": int(subject_id),
            "minutes": minutes,
        },
    ).get("session")


def get_study_sessions():
    """Return completed sessions with their calculated minutes."""
    return _request(
        "GET",
        "/api/study/sessions",
    ).get("sessions", [])


def get_study_history():
    """Alias for dashboard study history."""
    return get_study_sessions()
