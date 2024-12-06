from utils import AchievementDatabase

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