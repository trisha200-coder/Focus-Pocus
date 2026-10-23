def get_study_summary(sessions, daily_goal=120):
    """Calculate summary statistics from study sessions."""
    total_minutes = sum(s.get("minutes", 0) for s in sessions)
    total_xp = sum(s.get("xp", 0) for s in sessions)
    level = total_xp // 200 + 1
    
    return {
        "total_study_time": f"{total_minutes // 60}h {total_minutes % 60}m",
        "total_minutes": total_minutes,
        "total_xp": total_xp,
        "level": level,
        "current_streak": len(set(s.get("date") for s in sessions if s.get("date"))),
        "daily_progress": f"{min(100, int((total_minutes / max(1, daily_goal)) * 100))}%"
    }

if __name__ == "__main__":
    from services.database import get_study_sessions, DatabaseAPIError
    try:
        sessions = get_study_sessions()
        summary = get_study_summary(sessions, daily_goal=120)
        print("Total study time:", summary["total_study_time"])
        print("Total XP:", summary["total_xp"])
        print("Level:", summary["level"])
        print("Current streak:", summary["current_streak"])
        print("Daily progress:", summary["daily_progress"])
    except DatabaseAPIError as error:
        print("Unable to load study history:", error)
