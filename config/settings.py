"""Configuration management for the application."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # AI API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    STABILITY_AI_API_KEY = os.getenv("STABILITY_AI_API_KEY")
    
    # LinkedIn
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    # Facebook/Instagram
    FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
    FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
    INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    
    # Application Settings
    POSTS_PER_DAY = int(os.getenv("POSTS_PER_DAY", 3))
    RESEARCH_TOPICS = os.getenv("RESEARCH_TOPICS", "amazon,e-commerce,business").split(",")
    TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/posts.db")
    
    @classmethod
    def validate(cls):
        """Validate that all required settings are present."""
        required = [
            "GROQ_API_KEY",
            "STABILITY_AI_API_KEY",
        ]
        
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True


settings = Settings()
