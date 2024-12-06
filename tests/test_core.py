import pytest
from utils import AchievementDatabase
from exceptions import ValidationError

class TestAchievementDatabase:
    """Core functionality tests"""
    
    def test_add_achievement(self, test_db, sample_achievement):
        test_db.add_achievement(sample_achievement)
        retrieved = test_db.get_achievement(sample_achievement["id"])
        assert retrieved["core"] == sample_achievement["core"]
    
    def test_validation(self, test_db):
        invalid_achievement = {"id": "INVALID"}
        with pytest.raises(ValidationError):
            test_db.add_achievement(invalid_achievement)