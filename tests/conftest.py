import pytest
from pathlib import Path
from typing import Dict, Any
from utils import AchievementDatabase

@pytest.fixture
def sample_achievement() -> Dict[str, Any]:
    return {
        "id": "TEST001",
        "core": "Test achievement",
        "dates": {"start": "2024-01", "end": "present"},
        "variations": {
            "technical_ic": {
                "short": "Test short",
                "medium": "Test medium",
                "detailed": "Test detailed"
            }
        },
        "metrics": [
            {
                "value": "50%",
                "context": "improvement",
                "verified": True
            }
        ],
        "impact": ["Test impact"]
    }

@pytest.fixture
def test_db(tmp_path: Path):
    return AchievementDatabase(base_dir=tmp_path)