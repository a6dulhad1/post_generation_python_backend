"""Image generation service using Stability AI."""
import os
import base64
import requests
from PIL import Image
from io import BytesIO
from config.settings import settings
from loguru import logger


class ImageGenerator:
    """Generate images using Stability AI."""
    
    def __init__(self):
        self.api_key = settings.STABILITY_AI_API_KEY
        self.api_host = "https://api.stability.ai"
        self.engine_id = "stable-diffusion-xl-1024-v1-0"
    
    def generate_image(self, prompt: str, output_path: str, 
                      width: int = 1024, height: int = 1024,
                      style: str = "professional") -> str:
        """
        Generate an image from text prompt.
        
        Args:
            prompt: Image description
            output_path: Path to save the generated image
            width: Image width (default 1024)
            height: Image height (default 1024)
            style: Style preset (professional, digital-art, photographic)
            
        Returns:
            Path to the generated image
        """
        # Enhance prompt for better results
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        url = f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": enhanced_prompt,
                    "weight": 1
                },
                {
                    "text": "blurry, bad quality, distorted, low resolution, watermark",
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": 30,
        }
        
        try:
            logger.info(f"Generating image with prompt: {prompt[:50]}...")
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code != 200:
                logger.error(f"API Error: {response.text}")
                raise Exception(f"Image generation failed: {response.status_code}")
            
            data = response.json()
            
            # Save the image
            for i, image_data in enumerate(data["artifacts"]):
                # Handle base64 data (could be actual base64 or hex)
                import base64
                try:
                    # Try base64 decoding first
                    image_bytes = base64.b64decode(image_data["base64"])
                except:
                    # Fallback to hex if base64 fails
                    image_bytes = bytes.fromhex(image_data["base64"])
                
                image = Image.open(BytesIO(image_bytes))
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save image
                image.save(output_path, format="PNG")
                logger.info(f"Image saved to {output_path}")
                
                return output_path
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise
    
    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """Enhance the prompt with style modifiers."""
        style_modifiers = {
            "professional": "professional photography, business setting, clean, modern, high quality",
            "digital-art": "digital art, vibrant colors, modern design, artistic",
            "photographic": "photorealistic, detailed, high resolution, professional photography"
        }
        
        modifier = style_modifiers.get(style, style_modifiers["professional"])
        return f"{prompt}, {modifier}"
    
    def generate_from_template(self, template: str, custom_elements: dict) -> str:
        """
        Generate image from a template with custom elements.
        Useful for branded content with consistent style.
        
        Args:
            template: Base template description
            custom_elements: Dictionary of custom elements to add
            
        Returns:
            Path to generated image
        """
        # Combine template with custom elements
        prompt_parts = [template]
        for key, value in custom_elements.items():
            prompt_parts.append(f"{key}: {value}")
        
        final_prompt = ", ".join(prompt_parts)
        output_path = f"./data/images/template_{hash(final_prompt)}.png"
        
        return self.generate_image(final_prompt, output_path)
    
    def resize_for_platform(self, image_path: str, platform: str) -> str:
        """
        Resize image for specific platform requirements.
        
        Args:
            image_path: Path to original image
            platform: Target platform (LinkedIn, Instagram, Facebook)
            
        Returns:
            Path to resized image
        """
        dimensions = {
            "LinkedIn": (1200, 627),  # LinkedIn recommended
            "Instagram": (1080, 1080),  # Instagram square
            "Facebook": (1200, 630)   # Facebook recommended
        }
        
        target_size = dimensions.get(platform, (1024, 1024))
        
        try:
            image = Image.open(image_path)
            image = image.resize(target_size, Image.Resampling.LANCZOS)
            
            # Save resized image
            base, ext = os.path.splitext(image_path)
            resized_path = f"{base}_{platform.lower()}{ext}"
            image.save(resized_path, format="PNG")
            
            logger.info(f"Resized image for {platform}: {resized_path}")
            return resized_path
            
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            return image_path  # Return original if resize fails
