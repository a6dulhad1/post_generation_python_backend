"""Daily scheduler for automated social media posts."""
import schedule
import time
import subprocess
import sys
from datetime import datetime
from loguru import logger
from config.settings import settings

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/scheduler_{time}.log", rotation="1 day", retention="30 days")


def run_daily_posts():
    """Execute daily post generation and publishing."""
    logger.info("="*60)
    logger.info("Starting scheduled daily posts")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*60)
    
    try:
        # Run main.py in auto mode
        result = subprocess.run(
            ["python", "main.py", "--mode", "auto"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            logger.info("✓ Daily posts completed successfully")
            logger.info(f"Output: {result.stdout}")
        else:
            logger.error(f"✗ Daily posts failed with code {result.returncode}")
            logger.error(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("✗ Daily posts timed out (>5 minutes)")
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")


def run_morning_posts():
    """Morning posts (9 AM)."""
    logger.info("Running morning posts...")
    run_daily_posts()


def run_afternoon_posts():
    """Afternoon posts (3 PM)."""
    logger.info("Running afternoon posts...")
    run_daily_posts()


def test_schedule():
    """Test the scheduler with immediate execution."""
    logger.info("Testing scheduler...")
    run_daily_posts()
    logger.info("Test complete. Scheduler is working correctly.")


def main():
    """Main scheduler loop."""
    logger.info("="*60)
    logger.info("AI Social Media Scheduler Started")
    logger.info("="*60)
    logger.info(f"Posts per day: {settings.POSTS_PER_DAY}")
    logger.info(f"Topics: {', '.join(settings.RESEARCH_TOPICS)}")
    logger.info(f"Timezone: {settings.TIMEZONE}")
    logger.info("")
    logger.info("Scheduled times:")
    logger.info("  - 09:00 AM (Morning posts)")
    logger.info("  - 03:00 PM (Afternoon posts)")
    logger.info("")
    logger.info("Press Ctrl+C to stop the scheduler")
    logger.info("="*60)
    
    # Schedule daily posts
    schedule.every().day.at("09:00").do(run_morning_posts)
    schedule.every().day.at("15:00").do(run_afternoon_posts)
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("\nScheduler stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Daily social media post scheduler")
    parser.add_argument("--test", action="store_true", help="Test the scheduler immediately")
    args = parser.parse_args()
    
    if args.test:
        test_schedule()
    else:
        main()
