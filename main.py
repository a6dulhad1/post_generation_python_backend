"""Main application entry point."""
import sys
import click
from loguru import logger
from pathlib import Path

from config.settings import settings
from services.trend_research import TrendResearcher
from services.content_generator import ContentGenerator
from services.image_generator import ImageGenerator
from services.post_scheduler import PostScheduler
from database.post_history import PostHistory

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/app_{time}.log", rotation="1 day", retention="7 days")


@click.command()
@click.option('--mode', type=click.Choice(['auto', 'manual', 'generate-only']), 
              default='auto', help='Operation mode')
@click.option('--prompt', type=str, help='Custom prompt for manual mode')
@click.option('--image', type=click.Path(exists=True), help='Custom image path for manual mode')
@click.option('--topics', type=str, help='Comma-separated topics to research')
@click.option('--platforms', type=str, help='Comma-separated platforms (LinkedIn,Instagram,Facebook)')
@click.option('--schedule', is_flag=True, help='Schedule posts instead of posting immediately')
def main(mode, prompt, image, topics, platforms, schedule):
    """AI-powered social media automation system."""
    
    try:
        # Validate settings
        settings.validate()
        logger.info("Starting AI Social Media Automation System")
        
        # Initialize services
        trend_researcher = TrendResearcher()
        content_generator = ContentGenerator()
        image_generator = ImageGenerator()
        post_scheduler = PostScheduler()
        post_history = PostHistory()
        
        # Parse topics and platforms
        research_topics = topics.split(',') if topics else settings.RESEARCH_TOPICS
        target_platforms = platforms.split(',') if platforms else ['LinkedIn', 'Instagram', 'Facebook']
        
        if mode == 'auto':
            logger.info(f"Running in AUTO mode - generating {settings.POSTS_PER_DAY} posts")
            run_auto_mode(
                trend_researcher, content_generator, image_generator,
                post_scheduler, post_history, research_topics, 
                target_platforms, schedule
            )
        
        elif mode == 'manual':
            if not prompt:
                logger.error("Manual mode requires --prompt argument")
                sys.exit(1)
            
            logger.info("Running in MANUAL mode with custom prompt")
            run_manual_mode(
                trend_researcher, content_generator, image_generator,
                post_scheduler, post_history, prompt, image,
                target_platforms, schedule
            )
        
        elif mode == 'generate-only':
            logger.info("Running in GENERATE-ONLY mode (no posting)")
            run_generate_only(
                trend_researcher, content_generator, image_generator,
                research_topics
            )
        
        logger.info("Process completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


def run_auto_mode(trend_researcher, content_generator, image_generator,
                  post_scheduler, post_history, topics, platforms, schedule_posts):
    """Run automated daily post generation."""
    
    # Research trends and generate ideas
    ideas = trend_researcher.research_trends(topics, settings.POSTS_PER_DAY)
    
    for i, idea in enumerate(ideas):
        logger.info(f"Processing idea {i+1}/{len(ideas)}: {idea['topic']}")
        
        # Determine target platform
        platform = idea.get('platform', 'LinkedIn')
        if platform not in platforms:
            platform = platforms[0]  # Default to first platform
        
        # Generate content
        content = content_generator.generate_post_content(idea, platform)
        
        # Generate image
        image_path = f"./data/images/post_{i+1}_{platform.lower()}.png"
        image_generator.generate_image(
            content['image_prompt'],
            image_path,
            width=1024,
            height=1024
        )
        
        # Resize for platform
        final_image = image_generator.resize_for_platform(image_path, platform)
        
        # Post or schedule
        post_data = {
            'topic': idea['topic'],
            'text': content['text'],
            'hashtags': content['hashtags'],
            'image_path': final_image,
            'platform': platform
        }
        
        if schedule_posts:
            post_scheduler.schedule_post(post_data, i)
            logger.info(f"Scheduled post {i+1} for {platform}")
        else:
            post_scheduler.post_now(post_data)
            logger.info(f"Posted to {platform}")
        
        # Save to history
        post_history.add_post(post_data)


def run_manual_mode(trend_researcher, content_generator, image_generator,
                   post_scheduler, post_history, user_prompt, image_path,
                   platforms, schedule_posts):
    """Run manual mode with custom prompt."""
    
    # Generate idea from user prompt
    idea = trend_researcher.generate_custom_idea(user_prompt)
    
    # Determine platform
    platform = idea.get('platform', 'LinkedIn')
    if platform not in platforms:
        platform = platforms[0]
    
    # Generate content
    content = content_generator.generate_post_content(idea, platform)
    
    # Handle image
    if image_path:
        # Use provided image
        final_image = image_path
        logger.info(f"Using provided image: {image_path}")
    else:
        # Generate image
        output_path = "./data/images/manual_post.png"
        image_generator.generate_image(content['image_prompt'], output_path)
        final_image = image_generator.resize_for_platform(output_path, platform)
    
    # Prepare post data
    post_data = {
        'topic': idea['topic'],
        'text': content['text'],
        'hashtags': content['hashtags'],
        'image_path': final_image,
        'platform': platform
    }
    
    # Display preview
    logger.info("\n" + "="*50)
    logger.info("POST PREVIEW")
    logger.info("="*50)
    logger.info(f"Platform: {platform}")
    logger.info(f"Topic: {idea['topic']}")
    logger.info(f"\nText:\n{content['text']}")
    logger.info(f"\nHashtags: {content['hashtags']}")
    logger.info(f"\nImage: {final_image}")
    logger.info("="*50 + "\n")
    
    # Confirm before posting
    if click.confirm('Do you want to post this?', default=True):
        if schedule_posts:
            post_scheduler.schedule_post(post_data, 0)
            logger.info("Post scheduled")
        else:
            post_scheduler.post_now(post_data)
            logger.info("Posted successfully")
        
        # Save to history
        post_history.add_post(post_data)
    else:
        logger.info("Post cancelled")


def run_generate_only(trend_researcher, content_generator, image_generator, topics):
    """Generate content without posting."""
    
    ideas = trend_researcher.research_trends(topics, settings.POSTS_PER_DAY)
    
    logger.info("\n" + "="*50)
    logger.info("GENERATED POST IDEAS")
    logger.info("="*50)
    
    for i, idea in enumerate(ideas):
        logger.info(f"\nIdea {i+1}:")
        logger.info(f"Topic: {idea['topic']}")
        logger.info(f"Angle: {idea['angle']}")
        logger.info(f"Platform: {idea.get('platform', 'LinkedIn')}")
        logger.info(f"Key Points: {', '.join(idea['key_points'])}")
        
        # Generate content
        platform = idea.get('platform', 'LinkedIn')
        content = content_generator.generate_post_content(idea, platform)
        
        logger.info(f"\nGenerated Text:\n{content['text']}")
        logger.info(f"\nHashtags: {content['hashtags']}")
        
        # Save to file
        output_file = f"./data/generated/idea_{i+1}.txt"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Topic: {idea['topic']}\n")
            f.write(f"Platform: {platform}\n\n")
            f.write(content['text'])
            f.write(f"\n\n{content['hashtags']}")
        
        logger.info(f"Saved to: {output_file}")
        logger.info("-" * 50)


if __name__ == '__main__':
    main()
