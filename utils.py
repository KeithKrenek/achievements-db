# utils.py
from __future__ import annotations
import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from validators import DataValidator
from exceptions import DatabaseError, AchievementNotFoundError, ValidationError

class DescriptionLength(Enum):
    """Enumeration for standard description lengths."""
    SHORT = 'short'
    MEDIUM = 'medium'
    DETAILED = 'detailed'

class DatabaseError(Exception):
    """Base exception class for database operations."""
    pass

class AchievementNotFoundError(DatabaseError):
    """Raised when an achievement cannot be found."""
    pass

class ValidationError(DatabaseError):
    """Raised when achievement data fails validation."""
    pass

class AchievementDatabase:
    """
    Manages a database of professional achievements with sophisticated querying capabilities.
    
    Features:
    - CRUD operations for achievements
    - Advanced querying by roles, tags, and metrics
    - Data validation
    - Error handling
    - Logging
    """
    
    REQUIRED_FIELDS = {'id', 'core', 'dates', 'variations', 'metrics', 'impact'}
    
    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """
        Initialize the achievement database.
        
        Args:
            base_dir: Optional custom directory path for the database.
                     Defaults to script's parent directory if not provided.
        """
        self.base_dir = base_dir or Path(__file__).parent
        self.achievements_dir = self.base_dir / 'achievements'
        self.achievements_dir.mkdir(exist_ok=True)
        
        # Configure logging
        self._setup_logging()
        
        self.logger.info(f"Achievement database initialized at {self.achievements_dir}")
    
    def _setup_logging(self) -> None:
        """Configure logging for the database operations."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.FileHandler(self.base_dir / 'achievement_db.log')
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _validate_achievement(self, achievement_data: Dict[str, Any]) -> None:
        """
        Validate achievement data structure and content.
        
        Args:
            achievement_data: Dictionary containing achievement information.
            
        Raises:
            ValidationError: If the achievement data is invalid.
        """
        # Check required fields
        missing_fields = self.REQUIRED_FIELDS - set(achievement_data.keys())
        if missing_fields:
            raise ValidationError(f"Missing required fields: {missing_fields}")
        
        # Validate dates
        dates = achievement_data.get('dates', {})
        try:
            if 'start' in dates:
                datetime.strptime(dates['start'], '%Y-%m')
            if 'end' in dates and dates['end'] != 'present':
                datetime.strptime(dates['end'], '%Y-%m')
        except ValueError as e:
            raise ValidationError(f"Invalid date format: {e}")
    
    def add_achievement(self, achievement_data: Dict[str, Any]) -> None:
        """
        Add or update an achievement in the database.
        
        Args:
            achievement_data: Dictionary containing achievement information.
            
        Raises:
            ValidationError: If the achievement data is invalid.
        """
        try:
            self._validate_achievement(achievement_data)
            
            achievement_id = achievement_data['id']
            file_path = self.achievements_dir / f"{achievement_id}.json"
            
            # Add metadata
            achievement_data['_metadata'] = {
                'last_modified': datetime.now().isoformat(),
                'version': achievement_data.get('_metadata', {}).get('version', 0) + 1
            }
            
            with open(file_path, 'w') as f:
                json.dump(achievement_data, f, indent=2)
            
            self.logger.info(f"Achievement {achievement_id} successfully saved")
            
        except Exception as e:
            self.logger.error(f"Error adding achievement: {e}")
            raise
    
    def get_achievement(self, achievement_id: str) -> Dict[str, Any]:
        """
        Retrieve a single achievement by ID.
        
        Args:
            achievement_id: Unique identifier for the achievement.
            
        Returns:
            Dictionary containing achievement data.
            
        Raises:
            AchievementNotFoundError: If the achievement doesn't exist.
        """
        file_path = self.achievements_dir / f"{achievement_id}.json"
        try:
            with open(file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            raise AchievementNotFoundError(f"Achievement {achievement_id} not found")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding achievement {achievement_id}: {e}")
            raise DatabaseError(f"Error reading achievement {achievement_id}")
    
    def get_all_achievements(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieve all achievements from the database.
        
        Returns:
            Dictionary mapping achievement IDs to their data.
        """
        achievements = {}
        for file_path in self.achievements_dir.glob('*.json'):
            try:
                with open(file_path) as f:
                    achievement = json.load(f)
                    achievements[achievement['id']] = achievement
            except Exception as e:
                self.logger.error(f"Error reading {file_path}: {e}")
                continue
        return achievements
    
    def query_by_role(
        self,
        role_type: str,
        length: Union[str, DescriptionLength] = DescriptionLength.MEDIUM
    ) -> List[str]:
        """
        Query achievements by role type and description length.
        
        Args:
            role_type: Type of role to query for.
            length: Desired description length (short, medium, detailed).
            
        Returns:
            List of achievement descriptions matching the criteria.
        """
        if isinstance(length, str):
            length = DescriptionLength(length)
            
        results = []
        achievements = self.get_all_achievements()
        
        for achievement in achievements.values():
            variations = achievement.get('variations', {})
            if role_type in variations and length.value in variations[role_type]:
                results.append(variations[role_type][length.value])
        
        return results
    
    def query_by_tags(self, tags: List[str], require_all: bool = False) -> List[Dict[str, Any]]:
        """
        Query achievements by tags.
        
        Args:
            tags: List of tags to search for.
            require_all: If True, all tags must be present. If False, any tag matches.
            
        Returns:
            List of achievements matching the tag criteria.
        """
        results = []
        achievements = self.get_all_achievements()
        
        for achievement in achievements.values():
            achievement_tags = set(achievement.get('tags', []))
            if require_all:
                if all(tag in achievement_tags for tag in tags):
                    results.append(achievement)
            else:
                if any(tag in achievement_tags for tag in tags):
                    results.append(achievement)
        
        return results
    
    def query_by_metrics(
        self,
        metric_type: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Query achievements by metric values.
        
        Args:
            metric_type: Type of metric to query.
            min_value: Minimum metric value (inclusive).
            max_value: Maximum metric value (inclusive).
            
        Returns:
            List of achievements matching the metric criteria.
        """
        results = []
        achievements = self.get_all_achievements()
        
        for achievement in achievements.values():
            for metric in achievement.get('metrics', []):
                if metric['context'] == metric_type:
                    try:
                        value = float(metric['value'])
                        if ((min_value is None or value >= min_value) and
                            (max_value is None or value <= max_value)):
                            results.append(achievement)
                            break
                    except ValueError:
                        continue
        
        return results

# add_achievement.py
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

# generate_resume.py
from typing import Optional, List, Dict, Any

def generate_role_specific_resume(
    role_type: str,
    tags: Optional[List[str]] = None,
    length: Union[str, DescriptionLength] = DescriptionLength.DETAILED,
    require_all_tags: bool = False
) -> Dict[str, List[Any]]:
    """
    Generate a targeted resume based on role and tags.
    
    Args:
        role_type: Type of role to filter for.
        tags: Optional list of tags to further filter results.
        length: Desired description length.
        require_all_tags: Whether all tags must be present.
        
    Returns:
        Dictionary containing filtered achievements and relevant metrics.
    """
    db = AchievementDatabase()
    
    # Get achievements by role
    achievements = db.query_by_role(role_type, length)
    
    # Filter by tags if provided
    if tags:
        tag_filtered = db.query_by_tags(tags, require_all_tags)
        achievements = [a for a in achievements if a in tag_filtered]
    
    # Extract relevant metrics
    metrics = []
    for achievement in achievements:
        if 'metrics' in achievement:
            metrics.extend(achievement['metrics'])
    
    return {
        'achievements': achievements,
        'metrics': metrics
    }

# query_achievements.py
def query_achievements(
    role_type: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metric_type: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> Dict[str, Any]:
    """
    Comprehensive achievement query function.
    
    Args:
        role_type: Optional role type to filter by.
        tags: Optional list of tags to filter by.
        metric_type: Optional metric type to filter by.
        min_value: Optional minimum metric value.
        max_value: Optional maximum metric value.
        
    Returns:
        Dictionary containing query results and summary statistics.
    """
    db = AchievementDatabase()
    results = {}
    
    if role_type:
        results['by_role'] = db.query_by_role(role_type)
    
    if tags:
        results['by_tags'] = db.query_by_tags(tags)
    
    if metric_type:
        results['by_metrics'] = db.query_by_metrics(metric_type, min_value, max_value)
    
    # Add summary statistics
    results['summary'] = {
        'total_matches': len(set().union(*results.values())),
        'query_parameters': {
            'role_type': role_type,
            'tags': tags,
            'metric_type': metric_type,
            'value_range': f"{min_value or 'min'}-{max_value or 'max'}"
        }
    }
    
    return results