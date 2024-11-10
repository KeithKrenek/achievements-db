from utils import AchievementDatabase

def generate_role_specific_resume(role_type, tags=None):
    db = AchievementDatabase()
    
    # Get achievements by role
    achievements = db.query_by_role(role_type, 'detailed')
    
    # Filter by tags if provided
    if tags:
        achievements = [a for a in achievements 
                       if any(tag in a['tags'] for tag in tags)]
    
    return achievements

if __name__ == "__main__":
    # Example usage
    technical_achievements = generate_role_specific_resume('technical_ic', 
                                                         ['AI/ML', 'Software'])
    print(technical_achievements)