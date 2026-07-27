"""Utility helper functions."""
import os
import hashlib
from datetime import datetime
from PIL import Image
from loguru import logger


def ensure_directory(path: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    os.makedirs(path, exist_ok=True)


def get_file_hash(file_path: str) -> str:
    """Get MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_timestamp() -> str:
    """Get current timestamp as string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def validate_image(image_path: str, max_size_mb: int = 5) -> bool:
    """
    Validate image file.
    
    Args:
        image_path: Path to image file
        max_size_mb: Maximum file size in MB
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check file exists
        if not os.path.exists(image_path):
            logger.error(f"Image not found: {image_path}")
            return False
        
        # Check file size
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            logger.error(f"Image too large: {file_size_mb:.2f}MB (max {max_size_mb}MB)")
            return False
        
        # Check if valid image
        img = Image.open(image_path)
        img.verify()
        
        # Check format
        if img.format not in ['PNG', 'JPEG', 'JPG']:
            logger.error(f"Unsupported format: {img.format}")
            return False
        
        logger.info(f"Image validation passed: {image_path}")
        return True
        
    except Exception as e:
        logger.error(f"Image validation failed: {e}")
        return False


def resize_image(input_path: str, output_path: str, max_width: int, max_height: int) -> str:
    """
    Resize image to fit within max dimensions while maintaining aspect ratio.
    
    Args:
        input_path: Path to input image
        output_path: Path to save resized image
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Path to resized image
    """
    img = Image.open(input_path)
    
    # Calculate aspect ratio
    aspect = img.width / img.height
    
    if img.width > max_width or img.height > max_height:
        if aspect > 1:  # Wider than tall
            new_width = max_width
            new_height = int(max_width / aspect)
        else:  # Taller than wide
            new_height = max_height
            new_width = int(max_height * aspect)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    img.save(output_path, format='PNG')
    logger.info(f"Resized image saved: {output_path}")
    
    return output_path


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length with suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_hashtags(text: str) -> list:
    """Extract hashtags from text."""
    words = text.split()
    hashtags = [word for word in words if word.startswith('#')]
    return hashtags


def format_post_preview(post_data: dict) -> str:
    """Format post data for preview display."""
    preview = f"""
{'='*60}
PLATFORM: {post_data.get('platform', 'N/A')}
TOPIC: {post_data.get('topic', 'N/A')}
{'='*60}

TEXT:
{post_data.get('text', 'N/A')}

HASHTAGS:
{post_data.get('hashtags', 'N/A')}

IMAGE:
{post_data.get('image_path', 'N/A')}
{'='*60}
"""
    return preview


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_optimal_posting_times() -> list:
    """
    Get optimal posting times based on platform best practices.
    
    Returns:
        List of (platform, hour) tuples
    """
    return [
        ('LinkedIn', 9),   # 9 AM - Business hours
        ('Instagram', 12), # 12 PM - Lunch break
        ('Facebook', 15),  # 3 PM - Afternoon engagement
    ]


def calculate_engagement_score(likes: int, comments: int, shares: int) -> float:
    """
    Calculate simple engagement score.
    
    Weights: comments > shares > likes
    """
    return (comments * 3) + (shares * 2) + (likes * 1)


def is_business_hours(hour: int = None) -> bool:
    """Check if current time or given hour is within business hours (8 AM - 6 PM)."""
    if hour is None:
        hour = datetime.now().hour
    return 8 <= hour <= 18


def generate_post_id() -> str:
    """Generate unique post ID."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_hash = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    return f"POST_{timestamp}_{random_hash}"
