from typing import Optional, List, Dict, Any
from utils import AchievementDatabase

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