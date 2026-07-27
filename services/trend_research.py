"""Trend research service using Groq API."""
import json
from groq import Groq
from config.settings import settings
from loguru import logger


class TrendResearcher:
    """Research trends and generate post ideas."""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "openai/gpt-oss-20b"
    
    def research_trends(self, topics: list[str], num_ideas: int = 3) -> list[dict]:
        """
        Research current trends and generate post ideas.
        
        Args:
            topics: List of topics to research
            num_ideas: Number of post ideas to generate
            
        Returns:
            List of post ideas with topic, angle, and key points
        """
        topics_str = ", ".join(topics)
        
        prompt = f"""You are a social media expert researching trends for LinkedIn, Instagram, and Facebook.
        
Research current trends and news about: {topics_str}

Generate {num_ideas} unique post ideas that would engage business professionals and entrepreneurs.

For each idea, provide:
1. Topic/Theme
2. Angle (what makes it interesting/valuable)
3. Key points to cover (3-5 bullet points)
4. Target audience
5. Best platform (LinkedIn, Instagram, or Facebook)

Return ONLY a JSON array with this structure:
[
  {{
    "topic": "...",
    "angle": "...",
    "key_points": ["...", "..."],
    "target_audience": "...",
    "platform": "LinkedIn"
  }}
]
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            ideas = json.loads(content)
            logger.info(f"Generated {len(ideas)} post ideas")
            return ideas
            
        except Exception as e:
            logger.error(f"Error researching trends: {e}")
            raise
    
    def generate_custom_idea(self, user_prompt: str, context: str = None) -> dict:
        """
        Generate a post idea from user's custom prompt.
        
        Args:
            user_prompt: User's description or prompt
            context: Optional additional context
            
        Returns:
            Post idea dictionary
        """
        prompt = f"""You are a social media expert. A user wants to create a post about:

"{user_prompt}"

{f'Additional context: {context}' if context else ''}

Generate a compelling post idea that would work well on LinkedIn, Instagram, and Facebook.

Provide:
1. Topic/Theme
2. Angle (what makes it interesting/valuable)
3. Key points to cover (3-5 bullet points)
4. Target audience
5. Recommended platform

Return ONLY a JSON object with this structure:
{{
  "topic": "...",
  "angle": "...",
  "key_points": ["...", "..."],
  "target_audience": "...",
  "platform": "LinkedIn"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            idea = json.loads(content)
            logger.info(f"Generated custom post idea: {idea['topic']}")
            return idea
            
        except Exception as e:
            logger.error(f"Error generating custom idea: {e}")
            raise
