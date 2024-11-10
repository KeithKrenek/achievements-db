import json
import os
from datetime import datetime
from pathlib import Path

class AchievementDatabase:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or Path(__file__).parent
        self.achievements_dir = self.base_dir / 'achievements'
        self.achievements_dir.mkdir(exist_ok=True)
        
    def add_achievement(self, achievement_data):
        """Add or update an achievement."""
        achievement_id = achievement_data['id']
        file_path = self.achievements_dir / f"{achievement_id}.json"
        
        with open(file_path, 'w') as f:
            json.dump(achievement_data, f, indent=2)
            
    def get_achievement(self, achievement_id):
        """Retrieve a single achievement."""
        file_path = self.achievements_dir / f"{achievement_id}.json"
        if file_path.exists():
            with open(file_path) as f:
                return json.load(f)
        return None
        
    def get_all_achievements(self):
        """Retrieve all achievements."""
        achievements = {}
        for file_path in self.achievements_dir.glob('*.json'):
            with open(file_path) as f:
                achievement = json.load(f)
                achievements[achievement['id']] = achievement
        return achievements
        
    def query_by_role(self, role_type, length='medium'):
        """Query achievements by role type and description length."""
        results = []
        for achievement in self.get_all_achievements().values():
            variations = achievement.get('variations', {})
            if role_type in variations:
                results.append(variations[role_type][length])
        return results
        
    def query_by_tags(self, tags):
        """Query achievements by tags."""
        results = []
        for achievement in self.get_all_achievements().values():
            if any(tag in achievement.get('tags', []) for tag in tags):
                results.append(achievement)
        return results