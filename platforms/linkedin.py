"""LinkedIn posting integration."""
import requests
from config.settings import settings
from loguru import logger


class LinkedInPoster:
    """Post content to LinkedIn."""
    
    def __init__(self):
        self.access_token = settings.LINKEDIN_ACCESS_TOKEN
        self.api_version = "v2"
        self.base_url = f"https://api.linkedin.com/{self.api_version}"
    
    def post(self, text: str, image_path: str = None) -> dict:
        """
        Post to LinkedIn.
        
        Args:
            text: Post text content
            image_path: Optional path to image
            
        Returns:
            Response from LinkedIn API
        """
        if not self.access_token:
            logger.warning("LinkedIn access token not configured")
            return self._mock_post("LinkedIn", text, image_path)
        
        try:
            # Get user profile info
            profile = self._get_profile()
            person_urn = profile['id']
            
            if image_path:
                # Upload image and create post with media
                return self._post_with_image(person_urn, text, image_path)
            else:
                # Create text-only post
                return self._post_text_only(person_urn, text)
                
        except Exception as e:
            logger.error(f"LinkedIn posting error: {e}")
            raise
    
    def _get_profile(self) -> dict:
        """Get current user's profile information."""
        url = f"{self.base_url}/me"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def _post_text_only(self, person_urn: str, text: str) -> dict:
        """Create a text-only post."""
        url = f"{self.base_url}/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        payload = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        logger.info("LinkedIn text post created successfully")
        return response.json()
    
    def _post_with_image(self, person_urn: str, text: str, image_path: str) -> dict:
        """Create a post with an image."""
        # Step 1: Register image upload
        register_url = f"{self.base_url}/assets?action=registerUpload"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:person:{person_urn}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        
        register_response = requests.post(register_url, headers=headers, json=register_payload)
        register_response.raise_for_status()
        register_data = register_response.json()
        
        # Step 2: Upload image
        upload_url = register_data['value']['uploadMechanism'][
            'com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset_urn = register_data['value']['asset']
        
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        upload_headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        
        upload_response = requests.put(upload_url, headers=upload_headers, data=image_data)
        upload_response.raise_for_status()
        
        # Step 3: Create post with uploaded image
        post_url = f"{self.base_url}/ugcPosts"
        post_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        post_payload = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_urn
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        post_response = requests.post(post_url, headers=post_headers, json=post_payload)
        post_response.raise_for_status()
        
        logger.info("LinkedIn image post created successfully")
        return post_response.json()
    
    def _mock_post(self, platform: str, text: str, image_path: str) -> dict:
        """Mock post for testing without credentials."""
        logger.warning(f"Mock posting to {platform} (no credentials configured)")
        logger.info(f"Text: {text[:100]}...")
        if image_path:
            logger.info(f"Image: {image_path}")
        
        return {
            "success": True,
            "platform": platform,
            "mock": True,
            "message": "Mock post (configure credentials for real posting)"
        }
