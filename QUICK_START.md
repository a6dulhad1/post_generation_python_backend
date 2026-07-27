# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Your API Keys

#### Required (Free):
- **Groq**: https://console.groq.com → Create API key

#### Required (Paid - has free credits):
- **Stability AI**: https://platform.stability.ai → Create API key, add credits

#### Optional (for posting):
- **LinkedIn**: https://www.linkedin.com/developers
- **Facebook/Instagram**: https://developers.facebook.com

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your Groq and Stability AI keys
```

Minimum `.env` configuration:
```
GROQ_API_KEY=gsk_your_key_here
STABILITY_AI_API_KEY=sk_your_key_here
```

### 4. Test Your Setup
```bash
python utils/test_apis.py
```

### 5. Generate Your First Post Ideas
```bash
python main.py --mode generate-only --topics "amazon,business,AI"
```

Check `./data/generated/` for the results!

## Usage Examples

### Generate Ideas (No Posting)
```bash
python main.py --mode generate-only
```

### Manual Post with Custom Prompt
```bash
python main.py --mode manual --prompt "Just closed a $250,000 deal!"
```

### Manual Post with Screenshot
```bash
python main.py --mode manual --prompt "Excited to share our Q4 results" --image ./screenshot.png
```

### Automated Daily Posts
```bash
python main.py --mode auto
```

### Specify Topics
```bash
python main.py --mode auto --topics "AI,technology,startups"
```

### Specify Platforms
```bash
python main.py --mode auto --platforms "LinkedIn,Instagram"
```

### Schedule Posts (Instead of Immediate)
```bash
python main.py --mode auto --schedule
```

## What Gets Generated?

For each post idea, the system generates:
1. **Topic & Angle** - What to post about and why it's interesting
2. **Post Text** - Platform-optimized content (150-200 words)
3. **Hashtags** - 5-10 relevant hashtags
4. **AI Image** - Custom generated image using Stability AI
5. **Platform Optimization** - Resized and formatted for each platform

## Directory Structure After First Run

```
project/
├── data/
│   ├── images/           # Generated images
│   ├── generated/        # Generated text content
│   └── posts.db          # Post history database
├── logs/                 # Application logs
└── ...
```

## Next Steps

### Set Up Social Media Posting
See `SETUP_GUIDE.md` for detailed instructions on:
- LinkedIn OAuth setup
- Facebook/Instagram API configuration
- Getting access tokens

### Automate Daily Posts

**Option 1: Python Scheduler**
```python
# Create daily_scheduler.py
import schedule
import time
import subprocess

def run_daily_posts():
    subprocess.run(["python", "main.py", "--mode", "auto"])

schedule.every().day.at("09:00").do(run_daily_posts)

while True:
    schedule.run_pending()
    time.sleep(60)
```

**Option 2: Cron (Linux/Mac)**
```bash
crontab -e
# Add: 0 9 * * * cd /path/to/project && python main.py --mode auto
```

**Option 3: Windows Task Scheduler**
- Create a scheduled task to run `python main.py --mode auto` daily

### Customize Content

Edit these files to customize:
- `services/trend_research.py` - Research prompts and topics
- `services/content_generator.py` - Content style and tone
- `services/image_generator.py` - Image styles and templates

### View Post History
```python
from database.post_history import PostHistory

history = PostHistory()
recent = history.get_recent_posts(limit=10)
stats = history.get_stats()

print(f"Total posts: {stats['total_posts']}")
print(f"This week: {stats['posts_this_week']}")
```

## Tips for Best Results

1. **Start with generate-only mode** to review content quality
2. **Test manual mode** before automating
3. **Customize research topics** to your niche
4. **Review and refine** generated content initially
5. **Monitor engagement** and adjust topics/style accordingly

## Troubleshooting

**"Missing API key"**
- Check your `.env` file has `GROQ_API_KEY` and `STABILITY_AI_API_KEY`

**"Image generation failed"**
- Ensure you have credits in your Stability AI account
- Check your API key is correct

**"No ideas generated"**
- Check Groq API is working: `python utils/test_apis.py`
- Try simpler topics

**"Mock posting"**
- This is normal if you haven't configured social media APIs
- The system will show what would be posted without actually posting

## Common Use Cases

### 1. Daily Business Updates
```bash
# Morning: Generate ideas
python main.py --mode generate-only --topics "business,entrepreneurship"

# Afternoon: Post manually after review
python main.py --mode manual --prompt "Your chosen topic"
```

### 2. Product Launch Campaign
```bash
python main.py --mode manual --prompt "Launching our new AI feature today!" --platforms "LinkedIn,Facebook,Instagram"
```

### 3. Achievement Sharing
```bash
python main.py --mode manual --prompt "Reached 10,000 customers milestone" --image ./milestone_screenshot.png
```

### 4. Fully Automated
```bash
# Set up once, runs daily automatically
python main.py --mode auto --schedule
```

## Support & Resources

- Full setup guide: `SETUP_GUIDE.md`
- Code examples: `examples/example_usage.py`
- Test APIs: `python utils/test_apis.py`
- Check logs: `logs/` directory

## Important Notes

⚠ **Always review generated content** before posting to ensure it aligns with your brand voice

⚠ **Respect platform policies** - don't spam, follow posting limits

⚠ **Keep credentials secure** - never commit `.env` file

⚠ **Start slowly** - test with 1-2 posts before full automation

✅ **Have fun** and let AI handle the content creation!
