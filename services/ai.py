import os
import requests

API_URL = os.getenv(
    "FOCUS_POCUS_API_URL",
    "http://localhost:3000"
)


def get_ai_response(message: str) -> str:
    """Send a message to Express and return the AI response."""

    if not message or not message.strip():
        return "Please enter a message."

    try:
        response = requests.post(
            f"{API_URL}/api/chat",
            json={"message": message.strip()},
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()

        reply = data.get("reply")
        if not isinstance(reply, str) or not reply.strip():
            return "The AI service returned an empty response."

        return reply

    except requests.RequestException:
        return (
            "Unable to connect to Focus-Pocus AI. "
            "Please check that the Express backend is running."
        )
