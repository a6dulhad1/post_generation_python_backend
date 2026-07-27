"""Test script to verify API connections."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import settings
from services.trend_research import TrendResearcher
from services.content_generator import ContentGenerator
from services.image_generator import ImageGenerator
from platforms.linkedin import LinkedInPoster
from platforms.instagram import InstagramPoster
from platforms.facebook import FacebookPoster
from loguru import logger


def test_groq_api():
    """Test Groq API connection."""
    logger.info("Testing Groq API...")
    try:
        researcher = TrendResearcher()
        ideas = researcher.research_trends(["test"], num_ideas=1)
        
        if ideas and len(ideas) > 0:
            logger.info("✓ Groq API: Connected successfully")
            logger.info(f"  Sample idea: {ideas[0].get('topic', 'N/A')}")
            return True
        else:
            logger.error("✗ Groq API: No ideas generated")
            return False
            
    except Exception as e:
        logger.error(f"✗ Groq API: Failed - {e}")
        return False


def test_stability_ai():
    """Test Stability AI connection."""
    logger.info("Testing Stability AI...")
    try:
        generator = ImageGenerator()
        
        # Try to generate a small test image
        test_prompt = "A simple professional logo"
        output_path = "./data/test_image.png"
        
        result = generator.generate_image(
            test_prompt,
            output_path,
            width=1024,  # Changed to valid SDXL dimension
            height=1024  # Changed to valid SDXL dimension
        )
        
        if result and Path(output_path).exists():
            logger.info("✓ Stability AI: Connected successfully")
            logger.info(f"  Test image saved: {output_path}")
            return True
        else:
            logger.error("✗ Stability AI: Image generation failed")
            return False
            
    except Exception as e:
        logger.error(f"✗ Stability AI: Failed - {e}")
        return False


def test_linkedin_api():
    """Test LinkedIn API connection."""
    logger.info("Testing LinkedIn API...")
    
    if not settings.LINKEDIN_ACCESS_TOKEN:
        logger.warning("⚠ LinkedIn: No access token configured (skipping)")
        return None
    
    try:
        poster = LinkedInPoster()
        profile = poster._get_profile()
        
        if profile:
            logger.info("✓ LinkedIn API: Connected successfully")
            logger.info(f"  Profile ID: {profile.get('id', 'N/A')}")
            return True
        else:
            logger.error("✗ LinkedIn API: Failed to get profile")
            return False
            
    except Exception as e:
        logger.error(f"✗ LinkedIn API: Failed - {e}")
        return False


def test_facebook_api():
    """Test Facebook API connection."""
    logger.info("Testing Facebook API...")
    
    if not settings.FACEBOOK_ACCESS_TOKEN:
        logger.warning("⚠ Facebook: No access token configured (skipping)")
        return None
    
    try:
        poster = FacebookPoster()
        pages = poster.get_pages()
        
        if pages:
            logger.info("✓ Facebook API: Connected successfully")
            logger.info(f"  Found {len(pages)} page(s)")
            for page in pages:
                logger.info(f"    - {page.get('name', 'N/A')} (ID: {page.get('id', 'N/A')})")
            return True
        else:
            logger.warning("⚠ Facebook API: No pages found")
            return False
            
    except Exception as e:
        logger.error(f"✗ Facebook API: Failed - {e}")
        return False


def test_instagram_api():
    """Test Instagram API connection."""
    logger.info("Testing Instagram API...")
    
    if not settings.FACEBOOK_ACCESS_TOKEN or not settings.INSTAGRAM_BUSINESS_ACCOUNT_ID:
        logger.warning("⚠ Instagram: No credentials configured (skipping)")
        return None
    
    try:
        poster = InstagramPoster()
        info = poster.get_account_info()
        
        if info and 'id' in info:
            logger.info("✓ Instagram API: Connected successfully")
            logger.info(f"  Username: {info.get('username', 'N/A')}")
            logger.info(f"  Account Type: {info.get('account_type', 'N/A')}")
            logger.info(f"  Media Count: {info.get('media_count', 'N/A')}")
            return True
        else:
            logger.error("✗ Instagram API: Failed to get account info")
            return False
            
    except Exception as e:
        logger.error(f"✗ Instagram API: Failed - {e}")
        return False


def main():
    """Run all API tests."""
    logger.info("="*60)
    logger.info("API CONNECTION TESTS")
    logger.info("="*60)
    
    # Validate settings first
    try:
        settings.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.info("\nPlease configure your .env file with required API keys.")
        sys.exit(1)
    
    results = {
        "Groq API": test_groq_api(),
        "Stability AI": test_stability_ai(),
        "LinkedIn API": test_linkedin_api(),
        "Facebook API": test_facebook_api(),
        "Instagram API": test_instagram_api(),
    }
    
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    for service, result in results.items():
        if result is True:
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
        else:
            status = "⚠ SKIP"
        
        logger.info(f"{service}: {status}")
    
    # Count results
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    logger.info(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed > 0:
        logger.warning("\n⚠ Some tests failed. Please check your API credentials.")
        sys.exit(1)
    elif passed == 0:
        logger.warning("\n⚠ No tests passed. Please configure your API credentials.")
        sys.exit(1)
    else:
        logger.info("\n✓ All configured APIs are working!")


if __name__ == "__main__":
    main()
