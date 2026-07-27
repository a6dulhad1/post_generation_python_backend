"""Example usage scenarios for the AI Social Media Automation System."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.trend_research import TrendResearcher
from services.content_generator import ContentGenerator
from services.image_generator import ImageGenerator
from utils.helpers import format_post_preview


def example_1_research_trends():
    """Example: Research trends and generate post ideas."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Research Trends")
    print("="*60)
    
    researcher = TrendResearcher()
    
    # Research current trends
    topics = ["amazon", "e-commerce", "AI in business"]
    ideas = researcher.research_trends(topics, num_ideas=3)
    
    print(f"\nGenerated {len(ideas)} post ideas:\n")
    for i, idea in enumerate(ideas, 1):
        print(f"\n{i}. {idea['topic']}")
        print(f"   Angle: {idea['angle']}")
        print(f"   Platform: {idea.get('platform', 'LinkedIn')}")
        print(f"   Key Points:")
        for point in idea['key_points']:
            print(f"     - {point}")


def example_2_generate_content():
    """Example: Generate complete post content."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Generate Post Content")
    print("="*60)
    
    researcher = TrendResearcher()
    generator = ContentGenerator()
    
    # Generate idea
    idea = researcher.generate_custom_idea(
        "Just closed a $250,000 deal with a major client",
        context="B2B SaaS company, celebrating milestone"
    )
    
    print(f"\nTopic: {idea['topic']}")
    print(f"Target: {idea['target_audience']}")
    
    # Generate content for LinkedIn
    content = generator.generate_post_content(idea, "LinkedIn")
    
    print(f"\n--- LinkedIn Post ---")
    print(content['text'])
    print(f"\n{content['hashtags']}")
    print(f"\nImage Prompt: {content['image_prompt']}")


def example_3_generate_image():
    """Example: Generate AI image."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Generate AI Image")
    print("="*60)
    
    generator = ImageGenerator()
    
    prompt = "Professional business success celebration, modern office, team celebrating a major deal, vibrant colors, photorealistic"
    output_path = "./data/examples/example_image.png"
    
    print(f"\nPrompt: {prompt}")
    print("Generating image... (this may take 10-30 seconds)")
    
    try:
        result = generator.generate_image(
            prompt,
            output_path,
            width=1024,
            height=1024,
            style="professional"
        )
        print(f"\n✓ Image generated: {result}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_4_custom_manual_post():
    """Example: Create custom post with user input."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Manual Post")
    print("="*60)
    
    researcher = TrendResearcher()
    generator = ContentGenerator()
    
    # User's custom prompt
    user_prompt = """
    I just launched a new AI-powered feature for our product.
    It helps businesses automate their customer support responses
    and has already reduced response time by 70% in beta testing.
    """
    
    print(f"User Prompt: {user_prompt.strip()}")
    
    # Generate idea
    idea = researcher.generate_custom_idea(user_prompt)
    
    # Generate content
    content = generator.generate_post_content(idea, "LinkedIn")
    
    # Display preview
    post_data = {
        'platform': 'LinkedIn',
        'topic': idea['topic'],
        'text': content['text'],
        'hashtags': content['hashtags'],
        'image_path': 'generated_image.png'
    }
    
    print(format_post_preview(post_data))


def example_5_multi_platform():
    """Example: Generate content for multiple platforms."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Multi-Platform Content")
    print("="*60)
    
    researcher = TrendResearcher()
    generator = ContentGenerator()
    
    # Generate base idea
    idea = researcher.generate_custom_idea(
        "Sharing 5 productivity tips that helped me 10x my output"
    )
    
    platforms = ['LinkedIn', 'Instagram', 'Facebook']
    
    for platform in platforms:
        print(f"\n--- {platform} ---")
        content = generator.generate_post_content(idea, platform)
        print(f"\n{content['text']}\n")
        print(f"Hashtags: {content['hashtags']}")
        print("-" * 40)


def example_6_content_refinement():
    """Example: Refine content based on feedback."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Content Refinement")
    print("="*60)
    
    generator = ContentGenerator()
    
    original = """
    Just closed a huge deal! 🎉
    
    Really excited about this one. Been working on it for months.
    Can't wait to see what comes next!
    
    #success #business #deals
    """
    
    print("Original Post:")
    print(original)
    
    feedback = """
    Make it more professional, add specific details about the deal value,
    explain what problem this solves for the client, and use more
    business-focused hashtags.
    """
    
    print(f"\nFeedback: {feedback}")
    print("\nRefining content...")
    
    refined = generator.refine_content(original, feedback)
    
    print("\nRefined Post:")
    print(refined)


def main():
    """Run all examples."""
    examples = [
        ("Research Trends", example_1_research_trends),
        ("Generate Content", example_2_generate_content),
        ("Generate Image", example_3_generate_image),
        ("Custom Manual Post", example_4_custom_manual_post),
        ("Multi-Platform Content", example_5_multi_platform),
        ("Content Refinement", example_6_content_refinement),
    ]
    
    print("\n" + "="*60)
    print("AI SOCIAL MEDIA AUTOMATION - EXAMPLES")
    print("="*60)
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
    
    print("\n0. Run all examples")
    print("Q. Quit")
    
    choice = input("\nSelect an example (0-6, Q): ").strip().upper()
    
    if choice == 'Q':
        return
    elif choice == '0':
        for name, func in examples:
            try:
                func()
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"\nError in {name}: {e}")
                input("\nPress Enter to continue...")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        try:
            examples[int(choice) - 1][1]()
        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
