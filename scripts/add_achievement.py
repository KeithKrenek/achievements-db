from utils import AchievementDatabase

def add_new_achievement():
    """Interactive script to add new achievement."""
    db = AchievementDatabase()
    
    # Load achievement data (example)
    achievement_data = {
        "id": "ML001",
        "core": "Applied machine learning to improve production yield",
        # ... rest of the achievement data
    }
    
    db.add_achievement(achievement_data)

if __name__ == "__main__":
    add_new_achievement()