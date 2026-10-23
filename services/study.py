from services.database import get_study_sessions
from services.database import DatabaseAPIError
from services.study import get_study_summary

try:
    sessions = get_study_sessions()

    summary = get_study_summary(
        sessions,
        daily_goal=120
    )

    print("Total study time:", summary["total_study_time"])
    print("Total XP:", summary["total_xp"])
    print("Level:", summary["level"])
    print("Current streak:", summary["current_streak"])
    print("Daily progress:", summary["daily_progress"])

except DatabaseAPIError as error:
    print("Unable to load study history:", error)
