# Setup Guide - AI Social Media Automation System

## Step-by-Step Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Keys

#### Groq API (Text Generation)
1. Go to https://console.groq.com
2. Sign up for a free account
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

#### Stability AI (Image Generation)
1. Go to https://platform.stability.ai
2. Create an account
3. Go to Account > API Keys
4. Create a new API key
5. Add credits to your account (required for image generation)

### 3. Configure Social Media APIs

#### LinkedIn Setup
1. Go to https://www.linkedin.com/developers
2. Create a new app
3. Required permissions:
   - `w_member_social` (post on behalf of user)
   - `r_liteprofile` (get profile info)
4. Get Client ID and Client Secret
5. Generate Access Token using OAuth 2.0 flow
   - Use this tool: https://www.linkedin.com/developers/tools/oauth
   - Or implement OAuth flow in your app

**LinkedIn OAuth Flow:**
```python
# Step 1: Get authorization code
# Direct user to:
https://www.linkedin.com/oauth/v2/authorization?
  response_type=code&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=YOUR_REDIRECT_URI&
  scope=w_member_social%20r_liteprofile

# Step 2: Exchange code for access token
import requests

url = "https://www.linkedin.com/oauth/v2/accessToken"
data = {
    "grant_type": "authorization_code",
    "code": "AUTHORIZATION_CODE",
    "redirect_uri": "YOUR_REDIRECT_URI",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
}

response = requests.post(url, data=data)
access_token = response.json()["access_token"]
```

#### Facebook/Instagram Setup
1. Go to https://developers.facebook.com
2. Create a new app (Business type)
3. Add Instagram Graph API product
4. Required permissions:
   - `pages_manage_posts` (post to Facebook Page)
   - `pages_read_engagement` (read engagement data)
   - `instagram_basic` (Instagram access)
   - `instagram_content_publish` (post to Instagram)
5. Get App ID and App Secret
6. Generate User Access Token using Graph API Explorer
7. Convert to Long-Lived Token (60 days):

```python
import requests

url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": "YOUR_APP_ID",
    "client_secret": "YOUR_APP_SECRET",
    "fb_exchange_token": "SHORT_LIVED_TOKEN"
}

response = requests.get(url, params=params)
long_lived_token = response.json()["access_token"]
```

8. Get Instagram Business Account ID:
```python
# First, get your Facebook Page ID
url = "https://graph.facebook.com/v18.0/me/accounts"
params = {"access_token": "YOUR_ACCESS_TOKEN"}
response = requests.get(url, params=params)
page_id = response.json()["data"][0]["id"]

# Then, get Instagram Business Account ID
url = f"https://graph.facebook.com/v18.0/{page_id}"
params = {
    "fields": "instagram_business_account",
    "access_token": "YOUR_ACCESS_TOKEN"
}
response = requests.get(url, params=params)
ig_account_id = response.json()["instagram_business_account"]["id"]
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:
```bash
# AI API Keys
GROQ_API_KEY=gsk_your_groq_api_key_here
STABILITY_AI_API_KEY=sk-your_stability_ai_key_here

# LinkedIn Credentials
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

# Facebook/Instagram Credentials
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_long_lived_facebook_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_id

# Configuration
POSTS_PER_DAY=3
RESEARCH_TOPICS=amazon,e-commerce,business,entrepreneurship
TIMEZONE=America/New_York
DATABASE_PATH=./data/posts.db
```

### 5. Create Required Directories

```bash
mkdir -p data/images
mkdir -p data/generated
mkdir -p logs
```

### 6. Test the Setup

Test API connections:
```bash
python utils/test_apis.py
```

This will verify:
- Groq API connection
- Stability AI API connection
- Social media API connections

### 7. Run Your First Test

Generate ideas without posting:
```bash
python main.py --mode generate-only --topics "amazon,business"
```

### 8. Post Your First Update

Manual post with custom prompt:
```bash
python main.py --mode manual --prompt "Excited to share that I just closed a $250,000 deal!"
```

### 9. Setup Automated Daily Posts

Option A: Use Schedule (Python-based)
```python
# Create scheduler.py
from services.post_scheduler import PostScheduler
import main

scheduler = PostScheduler()

# Schedule for 9 AM, 12 PM, and 3 PM
for i, hour in enumerate([9, 12, 15]):
    schedule.every().day.at(f"{hour:02d}:00").do(
        main.run_auto_mode,
        # ... parameters
    )

scheduler.run_scheduler()
```

Option B: Use Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add daily posts at 9 AM
0 9 * * * cd /path/to/project && python main.py --mode auto
```

Option C: Use Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily at 9 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `main.py --mode auto`
7. Start in: `/path/to/project`

## Important Notes

### Rate Limits
- **LinkedIn**: 100 posts per day
- **Instagram**: 25 posts per day (Business accounts)
- **Facebook**: No strict limit, but avoid spam behavior

### Best Practices
1. Test with `--mode generate-only` first
2. Review generated content before posting
3. Start with manual posts to verify setup
4. Monitor engagement and adjust topics
5. Keep API credentials secure
6. Never commit `.env` file to version control

### Instagram Image Hosting
Instagram requires publicly accessible image URLs. Options:
1. **AWS S3**: Upload to S3 bucket with public read access
2. **Cloudinary**: Free tier available
3. **ImgBB**: Simple API for image hosting
4. **Your own server**: Host images with public URL

Example S3 integration:
```python
import boto3

s3 = boto3.client('s3')
bucket_name = 'your-bucket'

s3.upload_file(
    'local_image.png',
    bucket_name,
    'images/post.png',
    ExtraArgs={'ACL': 'public-read'}
)

image_url = f"https://{bucket_name}.s3.amazonaws.com/images/post.png"
```

### Troubleshooting

**"Access token expired"**
- Regenerate access tokens (LinkedIn/Facebook tokens expire)
- LinkedIn: 60 days
- Facebook: 60 days for long-lived tokens

**"Permission denied"**
- Verify app has required permissions
- User must approve permissions
- May need app review for production use

**"Image upload failed"**
- Check image format (PNG/JPEG)
- Verify file size (< 5MB recommended)
- Ensure image URL is publicly accessible (Instagram)

**"Rate limit exceeded"**
- Reduce POSTS_PER_DAY setting
- Add delays between posts
- Spread posts throughout the day

## Next Steps

1. Customize prompts in `services/trend_research.py`
2. Add your brand voice to content generation
3. Create custom image templates
4. Set up monitoring and analytics
5. Implement engagement tracking
6. Add notification webhooks

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review API documentation
3. Test individual components with test scripts
4. Enable debug logging in `main.py`
