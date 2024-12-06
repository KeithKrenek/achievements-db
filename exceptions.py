class DatabaseError(Exception):
    """Base exception class for database operations."""
    pass

class AchievementNotFoundError(DatabaseError):
    """Raised when an achievement cannot be found."""
    pass

class ValidationError(DatabaseError):
    """Raised when achievement data fails validation."""
    pass