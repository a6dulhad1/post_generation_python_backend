"""Instagram posting integration."""
import requests
import time
from config.settings import settings
from loguru import logger


class InstagramPoster:
    """Post content to Instagram."""
    
    def __init__(self):
        self.access_token = settings.FACEBOOK_ACCESS_TOKEN
        self.instagram_account_id = settings.INSTAGRAM_BUSINESS_ACCOUNT_ID
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    def post(self, caption: str, image_path: str) -> dict:
        """
        Post to Instagram (requires Business/Creator account).
        
        Args:
            caption: Post caption with hashtags
            image_path: Path to image file
            
        Returns:
            Response from Instagram API
        """
        if not self.access_token or not self.instagram_account_id:
            logger.warning("Instagram credentials not configured")
            return self._mock_post("Instagram", caption, image_path)
        
        try:
            # Step 1: Create media container
            container_id = self._create_media_container(caption, image_path)
            
            # Step 2: Publish the container
            result = self._publish_media(container_id)
            
            logger.info("Instagram post created successfully")
            return result
            
        except Exception as e:
            logger.error(f"Instagram posting error: {e}")
            raise
    
    def _create_media_container(self, caption: str, image_path: str) -> str:
        """
        Create a media container (Step 1 of posting).
        
        Note: The image must be hosted on a publicly accessible URL.
        For local images, you'll need to upload to a hosting service first.
        """
        url = f"{self.base_url}/{self.instagram_account_id}/media"
        
        # For this example, assume image_path is a URL
        # In production, you'd upload the local file to a hosting service first
        params = {
            "image_url": image_path,  # This should be a public URL
            "caption": caption,
            "access_token": self.access_token
        }
        
        response = requests.post(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        container_id = data.get('id')
        
        logger.info(f"Created media container: {container_id}")
        return container_id
    
    def _publish_media(self, container_id: str) -> dict:
        """Publish the media container (Step 2 of posting)."""
        url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
        
        params = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        
        # Wait a moment for media to be processed
        time.sleep(2)
        
        response = requests.post(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def upload_image_to_hosting(self, local_image_path: str) -> str:
        """
        Upload image to a hosting service and return public URL.
        
        Note: You'll need to implement this based on your hosting choice:
        - AWS S3
        - Cloudinary
        - ImgBB
        - Your own server
        
        For now, this is a placeholder.
        """
        # TODO: Implement image upload to hosting service
        logger.warning("Image hosting not implemented - using local path")
        return local_image_path
    
    def _mock_post(self, platform: str, caption: str, image_path: str) -> dict:
        """Mock post for testing without credentials."""
        logger.warning(f"Mock posting to {platform} (no credentials configured)")
        logger.info(f"Caption: {caption[:100]}...")
        logger.info(f"Image: {image_path}")
        
        return {
            "success": True,
            "platform": platform,
            "mock": True,
            "message": "Mock post (configure credentials for real posting)"
        }
    
    def get_account_info(self) -> dict:
        """Get Instagram Business Account information."""
        if not self.access_token or not self.instagram_account_id:
            return {"error": "Credentials not configured"}
        
        url = f"{self.base_url}/{self.instagram_account_id}"
        params = {
            "fields": "id,username,account_type,media_count",
            "access_token": self.access_token
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
