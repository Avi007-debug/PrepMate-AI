"""
Utility functions
"""
import uuid
from datetime import datetime


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return f"session_{uuid.uuid4().hex[:16]}_{int(datetime.now().timestamp())}"


def validate_difficulty(difficulty: str) -> bool:
    """Validate difficulty level"""
    valid_levels = ["easy", "medium", "hard"]
    return difficulty.lower() in valid_levels


def validate_role(role: str) -> bool:
    """Validate role input"""
    return bool(role and len(role.strip()) > 0)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
