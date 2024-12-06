from utils import AchievementDatabase

def add_new_achievement(achievement_data: Dict[str, Any]) -> None:
    """
    Add a new achievement to the database with validation.
    
    Args:
        achievement_data: Dictionary containing achievement information.
    """
    try:
        db = AchievementDatabase()
        db.add_achievement(achievement_data)
        print(f"Successfully added achievement {achievement_data['id']}")
    except DatabaseError as e:
        print(f"Error adding achievement: {e}")
        raise

if __name__ == "__main__":
    add_new_achievement()