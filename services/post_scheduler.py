"""Post scheduling and publishing service."""
import schedule
import time
from datetime import datetime, timedelta
from loguru import logger

from platforms.linkedin import LinkedInPoster
from platforms.instagram import InstagramPoster
from platforms.facebook import FacebookPoster


class PostScheduler:
    """Schedule and publish posts to social media platforms."""
    
    def __init__(self):
        self.linkedin = LinkedInPoster()
        self.instagram = InstagramPoster()
        self.facebook = FacebookPoster()
        
        self.scheduled_posts = []
    
    def post_now(self, post_data: dict) -> dict:
        """
        Post content immediately to the specified platform.
        
        Args:
            post_data: Dictionary containing post information
            
        Returns:
            Result dictionary with status and details
        """
        platform = post_data['platform']
        
        try:
            if platform == 'LinkedIn':
                result = self.linkedin.post(
                    text=f"{post_data['text']}\n\n{post_data['hashtags']}",
                    image_path=post_data['image_path']
                )
            
            elif platform == 'Instagram':
                result = self.instagram.post(
                    caption=f"{post_data['text']}\n\n{post_data['hashtags']}",
                    image_path=post_data['image_path']
                )
            
            elif platform == 'Facebook':
                result = self.facebook.post(
                    message=f"{post_data['text']}\n\n{post_data['hashtags']}",
                    image_path=post_data['image_path']
                )
            
            else:
                raise ValueError(f"Unknown platform: {platform}")
            
            logger.info(f"Successfully posted to {platform}")
            return result
            
        except Exception as e:
            logger.error(f"Error posting to {platform}: {e}")
            raise
    
    def schedule_post(self, post_data: dict, index: int) -> None:
        """
        Schedule a post for later.
        
        Args:
            post_data: Dictionary containing post information
            index: Index for staggering posts throughout the day
        """
        # Calculate posting time (stagger posts throughout the day)
        base_hour = 9  # Start at 9 AM
        hours_between = 3  # 3 hours between posts
        
        post_time = f"{base_hour + (index * hours_between):02d}:00"
        
        schedule.every().day.at(post_time).do(
            self._execute_scheduled_post,
            post_data=post_data
        )
        
        self.scheduled_posts.append({
            'data': post_data,
            'time': post_time,
            'platform': post_data['platform']
        })
        
        logger.info(f"Scheduled post for {post_time} on {post_data['platform']}")
    
    def _execute_scheduled_post(self, post_data: dict):
        """Execute a scheduled post."""
        try:
            self.post_now(post_data)
            logger.info(f"Executed scheduled post to {post_data['platform']}")
        except Exception as e:
            logger.error(f"Error executing scheduled post: {e}")
    
    def run_scheduler(self):
        """Run the scheduler (blocks, for daemon mode)."""
        logger.info("Starting post scheduler daemon...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def get_scheduled_posts(self) -> list:
        """Get list of scheduled posts."""
        return self.scheduled_posts
    
    def cancel_scheduled_post(self, index: int):
        """Cancel a scheduled post by index."""
        if 0 <= index < len(self.scheduled_posts):
            post = self.scheduled_posts.pop(index)
            logger.info(f"Cancelled scheduled post for {post['time']}")
        else:
            logger.warning(f"Invalid index: {index}")
    
    def post_to_all_platforms(self, post_data: dict) -> dict:
        """
        Post to all configured platforms.
        
        Args:
            post_data: Dictionary containing post information
            
        Returns:
            Dictionary with results for each platform
        """
        results = {}
        platforms = ['LinkedIn', 'Instagram', 'Facebook']
        
        for platform in platforms:
            try:
                platform_post = post_data.copy()
                platform_post['platform'] = platform
                
                result = self.post_now(platform_post)
                results[platform] = {'success': True, 'result': result}
                
                # Wait between posts to avoid rate limits
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to post to {platform}: {e}")
                results[platform] = {'success': False, 'error': str(e)}
        
        return results
