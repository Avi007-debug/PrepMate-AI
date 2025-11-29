"""
Utility functions for PrepMate-AI backend
"""
import uuid
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# ID Generation
# ============================================================================

def generate_session_id() -> str:
    """
    Generate a unique session ID
    
    Returns:
        Unique session identifier string
    """
    return f"session_{uuid.uuid4().hex[:16]}_{int(datetime.now().timestamp())}"


# ============================================================================
# Validation Functions
# ============================================================================

def validate_difficulty(difficulty: str) -> bool:
    """
    Validate difficulty level
    
    Args:
        difficulty: Difficulty level string
        
    Returns:
        True if valid, False otherwise
    """
    valid_levels = ["easy", "medium", "hard"]
    return difficulty.lower() in valid_levels


def validate_role(role: str) -> bool:
    """
    Validate role input
    
    Args:
        role: Role string
        
    Returns:
        True if valid, False otherwise
    """
    return bool(role and len(role.strip()) > 0)


def validate_topics(topics: List[str]) -> bool:
    """
    Validate topics list
    
    Args:
        topics: List of topic strings
        
    Returns:
        True if valid, False otherwise
    """
    return isinstance(topics, list) and len(topics) > 0 and all(isinstance(t, str) for t in topics)


# ============================================================================
# Score Utilities
# ============================================================================

def calculate_average_score(scores: List[float]) -> float:
    """
    Calculate average score from a list of scores
    
    Args:
        scores: List of numerical scores
        
    Returns:
        Average score, 0.0 if list is empty
    """
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def normalize_score(score: float, min_score: float = 0.0, max_score: float = 10.0) -> float:
    """
    Normalize score to 0-10 scale
    
    Args:
        score: Raw score
        min_score: Minimum possible score
        max_score: Maximum possible score
        
    Returns:
        Normalized score between 0 and 10
    """
    if max_score == min_score:
        return 5.0
    normalized = ((score - min_score) / (max_score - min_score)) * 10
    return round(max(0.0, min(10.0, normalized)), 2)


def get_score_category(score: float) -> str:
    """
    Categorize score into performance levels
    
    Args:
        score: Score value (0-10)
        
    Returns:
        Performance category string
    """
    if score >= 9:
        return "Outstanding"
    elif score >= 8:
        return "Excellent"
    elif score >= 6:
        return "Good"
    elif score >= 4:
        return "Fair"
    else:
        return "Needs Improvement"


# ============================================================================
# JSON Formatting Helpers
# ============================================================================

def format_interview_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format interview summary for JSON response
    
    Args:
        summary: Raw summary dictionary
        
    Returns:
        Formatted summary dictionary
    """
    # Ensure all datetime objects are converted to ISO format strings
    formatted = summary.copy()
    
    # Round all float values to 2 decimal places
    if "statistics" in formatted:
        for key, value in formatted["statistics"].items():
            if isinstance(value, float):
                formatted["statistics"][key] = round(value, 2)
    
    # Format topic performance scores
    if "topic_performance" in formatted:
        formatted["topic_performance"] = {
            topic: round(score, 2)
            for topic, score in formatted["topic_performance"].items()
        }
    
    return formatted


def to_json_response(data: Any, status: str = "success", message: str = "") -> Dict[str, Any]:
    """
    Create standardized JSON response
    
    Args:
        data: Response data
        status: Response status (success/error)
        message: Optional message
        
    Returns:
        Standardized response dictionary
    """
    response = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    
    if message:
        response["message"] = message
    
    return response


def parse_json_safe(json_string: str, default: Any = None) -> Any:
    """
    Safely parse JSON string
    
    Args:
        json_string: JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError) as e:
        log_error(f"JSON parsing error: {str(e)}")
        return default


# ============================================================================
# Text Utilities
# ============================================================================

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text
    """
    # Remove null bytes and control characters
    sanitized = text.replace('\x00', '').strip()
    return sanitized


# ============================================================================
# Error Handling
# ============================================================================

class InterviewError(Exception):
    """Base exception for interview-related errors"""
    pass


class SessionNotFoundError(InterviewError):
    """Raised when session is not found"""
    pass


class QuestionGenerationError(InterviewError):
    """Raised when question generation fails"""
    pass


class FeedbackGenerationError(InterviewError):
    """Raised when feedback generation fails"""
    pass


def handle_error(error: Exception, context: str = "") -> Dict[str, Any]:
    """
    Handle and format errors
    
    Args:
        error: Exception object
        context: Additional context about the error
        
    Returns:
        Error response dictionary
    """
    error_message = f"{context}: {str(error)}" if context else str(error)
    log_error(error_message)
    
    return {
        "error": error.__class__.__name__,
        "message": error_message,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# Logging Utilities
# ============================================================================

def log_info(message: str):
    """Log info message"""
    logger.info(message)


def log_warning(message: str):
    """Log warning message"""
    logger.warning(message)


def log_error(message: str):
    """Log error message"""
    logger.error(message)


def log_debug(message: str):
    """Log debug message"""
    logger.debug(message)


def log_api_request(endpoint: str, method: str, params: Optional[Dict] = None):
    """
    Log API request
    
    Args:
        endpoint: API endpoint
        method: HTTP method
        params: Request parameters
    """
    params_str = json.dumps(params) if params else "None"
    log_info(f"API Request - {method} {endpoint} | Params: {params_str}")


def log_api_response(endpoint: str, status_code: int, duration_ms: float):
    """
    Log API response
    
    Args:
        endpoint: API endpoint
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
    """
    log_info(f"API Response - {endpoint} | Status: {status_code} | Duration: {duration_ms}ms")


# ============================================================================
# Time Utilities
# ============================================================================

def format_duration(start_time: datetime, end_time: datetime) -> str:
    """
    Format duration between two timestamps
    
    Args:
        start_time: Start timestamp
        end_time: End timestamp
        
    Returns:
        Formatted duration string
    """
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()
