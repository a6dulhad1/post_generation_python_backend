"""Facebook posting integration."""
import requests
from config.settings import settings
from loguru import logger


class FacebookPoster:
    """Post content to Facebook."""
    
    def __init__(self):
        self.access_token = settings.FACEBOOK_ACCESS_TOKEN
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    def post(self, message: str, image_path: str = None) -> dict:
        """
        Post to Facebook Page.
        
        Args:
            message: Post message with hashtags
            image_path: Optional path to image
            
        Returns:
            Response from Facebook API
        """
        if not self.access_token:
            logger.warning("Facebook access token not configured")
            return self._mock_post("Facebook", message, image_path)
        
        try:
            # Get page ID (you'll need to configure this)
            page_id = self._get_page_id()
            
            if image_path:
                return self._post_with_photo(page_id, message, image_path)
            else:
                return self._post_text_only(page_id, message)
                
        except Exception as e:
            logger.error(f"Facebook posting error: {e}")
            raise
    
    def _get_page_id(self) -> str:
        """
        Get Facebook Page ID.
        
        Note: In production, you should configure this in settings.
        This method shows how to retrieve pages you manage.
        """
        url = f"{self.base_url}/me/accounts"
        params = {
            "access_token": self.access_token
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('data') and len(data['data']) > 0:
            # Return first page ID
            page_id = data['data'][0]['id']
            logger.info(f"Using Facebook Page ID: {page_id}")
            return page_id
        else:
            raise Exception("No Facebook Pages found for this account")
    
    def _post_text_only(self, page_id: str, message: str) -> dict:
        """Post text-only status to Facebook Page."""
        url = f"{self.base_url}/{page_id}/feed"
        
        params = {
            "message": message,
            "access_token": self.access_token
        }
        
        response = requests.post(url, params=params)
        response.raise_for_status()
        
        logger.info("Facebook text post created successfully")
        return response.json()
    
    def _post_with_photo(self, page_id: str, message: str, image_path: str) -> dict:
        """Post with photo to Facebook Page."""
        url = f"{self.base_url}/{page_id}/photos"
        
        params = {
            "message": message,
            "access_token": self.access_token
        }
        
        # Upload image file
        with open(image_path, 'rb') as image_file:
            files = {
                'source': image_file
            }
            
            response = requests.post(url, params=params, files=files)
            response.raise_for_status()
        
        logger.info("Facebook photo post created successfully")
        return response.json()
    
    def _post_with_photo_url(self, page_id: str, message: str, image_url: str) -> dict:
        """Post with photo URL to Facebook Page."""
        url = f"{self.base_url}/{page_id}/photos"
        
        params = {
            "url": image_url,
            "message": message,
            "access_token": self.access_token
        }
        
        response = requests.post(url, params=params)
        response.raise_for_status()
        
        logger.info("Facebook photo URL post created successfully")
        return response.json()
    
    def get_pages(self) -> list:
        """Get list of Facebook Pages the user manages."""
        url = f"{self.base_url}/me/accounts"
        params = {
            "access_token": self.access_token
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('data', [])
    
    def _mock_post(self, platform: str, message: str, image_path: str) -> dict:
        """Mock post for testing without credentials."""
        logger.warning(f"Mock posting to {platform} (no credentials configured)")
        logger.info(f"Message: {message[:100]}...")
        if image_path:
            logger.info(f"Image: {image_path}")
        
        return {
            "success": True,
            "platform": platform,
            "mock": True,
            "message": "Mock post (configure credentials for real posting)"
        }
