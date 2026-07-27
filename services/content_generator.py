"""Content generation service using Groq API."""
from groq import Groq
from config.settings import settings
from loguru import logger


class ContentGenerator:
    """Generate post text and hashtags using AI."""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "openai/gpt-oss-20b"
    
    def generate_post_content(self, idea: dict, platform: str) -> dict:
        """
        Generate complete post content for a specific platform.
        
        Args:
            idea: Post idea dictionary from TrendResearcher
            platform: Target platform (LinkedIn, Instagram, or Facebook)
            
        Returns:
            Dictionary with text, hashtags, and image_prompt
        """
        platform_guidelines = {
            "LinkedIn": "Professional tone, 150-200 words, focus on business value and insights",
            "Instagram": "Engaging and visual, 100-150 words, conversational tone, emoji-friendly",
            "Facebook": "Friendly and accessible, 100-200 words, community-focused"
        }
        
        guideline = platform_guidelines.get(platform, platform_guidelines["LinkedIn"])
        
        prompt = f"""Create a {platform} post based on this idea:

Topic: {idea['topic']}
Angle: {idea['angle']}
Key Points: {', '.join(idea['key_points'])}
Target Audience: {idea['target_audience']}

Guidelines: {guideline}

Provide:
1. Post text (engaging, well-formatted with line breaks)
2. 5-10 relevant hashtags
3. A detailed image description for AI image generation (describe the visual that would best complement this post)

Format your response as:
POST TEXT:
[post text here]

HASHTAGS:
[hashtags here, space-separated]

IMAGE PROMPT:
[detailed image description here]
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            
            # Parse the response
            parts = content.split("POST TEXT:")
            if len(parts) > 1:
                rest = parts[1]
            else:
                rest = content
            
            text_parts = rest.split("HASHTAGS:")
            post_text = text_parts[0].strip()
            
            if len(text_parts) > 1:
                hashtag_parts = text_parts[1].split("IMAGE PROMPT:")
                hashtags = hashtag_parts[0].strip()
                image_prompt = hashtag_parts[1].strip() if len(hashtag_parts) > 1 else ""
            else:
                hashtags = ""
                image_prompt = ""
            
            result = {
                "text": post_text,
                "hashtags": hashtags,
                "image_prompt": image_prompt,
                "platform": platform
            }
            
            logger.info(f"Generated content for {platform}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    def refine_content(self, content: str, feedback: str) -> str:
        """
        Refine content based on user feedback.
        
        Args:
            content: Original content
            feedback: User feedback
            
        Returns:
            Refined content
        """
        prompt = f"""Refine this social media post based on the feedback:

Original Post:
{content}

Feedback:
{feedback}

Provide the improved version maintaining the same general structure but addressing the feedback.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            refined = response.choices[0].message.content.strip()
            logger.info("Content refined based on feedback")
            return refined
            
        except Exception as e:
            logger.error(f"Error refining content: {e}")
            raise
