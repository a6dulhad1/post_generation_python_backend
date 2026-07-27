# Frequently Asked Questions (FAQ)

## General Questions

### What is this project?
An AI-powered social media automation system that generates and posts content to LinkedIn, Instagram, and Facebook. It uses Groq for text generation and Stability AI for images.

### How much does it cost?
- **AI APIs**: ~$2/month (Groq is free, Stability AI ~$2/month for 100 images)
- **Social Media APIs**: Free
- **Total**: Much cheaper than tools like Hootsuite ($50-200/month)

### Do I need coding experience?
Basic command line knowledge is helpful, but the setup guides are beginner-friendly. You just need to:
1. Install Python
2. Copy API keys
3. Run commands

### Is it legal to automate social media posts?
Yes, when using official platform APIs. However:
- Review each platform's terms of service
- Don't spam or post misleading content
- Use responsibly and ethically

---

## Technical Questions

### Which Python version do I need?
Python 3.8 or higher. Python 3.11 is recommended for best performance.

### Can I run this on a Raspberry Pi?
Yes! Works on Raspberry Pi 4 with 2GB+ RAM. Installation is the same as Linux.

### Does it work offline?
No, it requires internet connection for:
- AI API calls (Groq, Stability AI)
- Social media posting
- Trend research

### Can I customize the content style?
Yes! Edit these files:
- `services/trend_research.py` - Research prompts
- `services/content_generator.py` - Content style and tone
- `services/image_generator.py` - Image styles

### How do I change posting times?
Edit `daily_scheduler.py`:
```python
# Change these lines
schedule.every().day.at("09:00").do(run_morning_posts)
schedule.every().day.at("15:00").do(run_afternoon_posts)
```

---

## API & Credentials

### Where do I get API keys?

**Groq (Free)**
1. Visit https://console.groq.com
2. Sign up for free account
3. Go to API Keys
4. Create new key
5. Copy key (starts with `gsk_`)

**Stability AI (Paid)**
1. Visit https://platform.stability.ai
2. Create account
3. Add credits ($10 minimum)
4. Go to Account > API Keys
5. Create and copy key

**LinkedIn**
1. Visit https://www.linkedin.com/developers
2. Create new app
3. Get Client ID/Secret
4. Use OAuth 2.0 for access token

**Facebook/Instagram**
1. Visit https://developers.facebook.com
2. Create new app (Business type)
3. Add Instagram Graph API
4. Get App ID/Secret and access token

### How long do access tokens last?
- **Groq**: Permanent (until manually revoked)
- **Stability AI**: Permanent
- **LinkedIn**: 60 days
- **Facebook**: 60 days (long-lived token)

### Can I use a free alternative to Stability AI?
Currently, the code uses Stability AI, but you could modify it to use:
- DALL-E (OpenAI)
- Midjourney (via API)
- Free alternatives like Craiyon (quality may vary)

### Do I need all three social media accounts?
No! You can use any combination:
- Just LinkedIn
- Just Instagram
- All three
- Or use `--mode generate-only` with no social accounts

---

## Features & Usage

### How many posts per day?
Default is 3, configurable in `.env`:
```
POSTS_PER_DAY=3
```

You can change this to any number, but respect platform limits:
- LinkedIn: 100 posts/day
- Instagram: 25 posts/day (Business accounts)
- Facebook: No strict limit

### Can I schedule posts for specific times?
Yes! Two ways:
1. Use `--schedule` flag to schedule throughout the day
2. Edit `daily_scheduler.py` for custom times

### Can I post to only one platform at a time?
Yes:
```bash
python main.py --mode auto --platforms "LinkedIn"
```

### Can I review posts before they're published?
Yes! Use `--mode generate-only` first:
```bash
python main.py --mode generate-only
# Review generated content in data/generated/
# Then post manually with --mode manual
```

### Can I use my own images instead of AI-generated?
Yes:
```bash
python main.py --mode manual --prompt "Your message" --image path/to/image.png
```

### How do I post about specific topics?
```bash
python main.py --mode auto --topics "AI,technology,startups"
```

Or edit `.env`:
```
RESEARCH_TOPICS=AI,technology,startups,business
```

### Can I post a screenshot with context?
Yes! Perfect for sharing achievements:
```bash
python main.py --mode manual \
  --prompt "Just hit $250,000 in sales this month!" \
  --image ./sales_screenshot.png
```

---

## Content Quality

### How do I improve generated content quality?
1. **Be specific with topics**: "e-commerce growth strategies" vs "business"
2. **Customize prompts**: Edit `services/content_generator.py`
3. **Add your brand voice**: Modify the system prompts
4. **Review and refine**: Use `--mode generate-only` first

### Are posts unique each time?
Yes! The AI generates unique content every time. The database also checks for duplicates.

### Can posts be in different languages?
Yes! Modify the prompts in `services/content_generator.py` to specify language:
```python
prompt = f"""Create a Spanish LinkedIn post about...
```

### How do I add emojis?
They're automatically included based on platform:
- Instagram: More emojis
- LinkedIn: Professional, fewer emojis
- Facebook: Moderate emojis

Customize in `services/content_generator.py`.

---

## Troubleshooting

### "Module not found" errors
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "API key invalid" errors
Check your `.env` file:
- No spaces around `=`
- No quotes around values
- Keys are correct from API dashboards

### "Image generation failed"
Common causes:
1. No credits in Stability AI account
2. Invalid API key
3. Network issues
4. Prompt too long/complex

### "Permission denied" (LinkedIn/Facebook)
Your app needs proper permissions:
- LinkedIn: `w_member_social`, `r_liteprofile`
- Facebook: `pages_manage_posts`, `instagram_content_publish`

### "Rate limit exceeded"
You're posting too frequently. Solutions:
1. Reduce `POSTS_PER_DAY`
2. Spread posts throughout the day
3. Add delays between posts

### Posts aren't showing on social media
Check:
1. Access token is valid (not expired)
2. App has proper permissions
3. Check platform's review process (some need approval)
4. Look at error logs in `./logs/`

### Dashboard won't start
```bash
# Install Flask
pip install flask>=3.0.0

# Then start
python dashboard.py
```

---

## Advanced Usage

### Can I run this on a server?
Yes! Use:
```bash
# Background process
nohup python daily_scheduler.py &

# Or use systemd (Linux)
sudo systemctl enable social-media-bot
sudo systemctl start social-media-bot
```

### How do I backup my data?
Backup these locations:
- `.env` (credentials)
- `data/` (images and database)
- `logs/` (optional)

```bash
# Create backup
tar -czf backup.tar.gz .env data/ logs/

# Restore backup
tar -xzf backup.tar.gz
```

### Can I integrate with other tools?
Yes! The system exposes:
- REST API (if using dashboard.py)
- Database (SQLite, easily queryable)
- Python modules (importable)

### How do I add more platforms (Twitter, TikTok)?
1. Create new file in `platforms/` (e.g., `twitter.py`)
2. Implement the posting logic
3. Add to `post_scheduler.py`
4. Update configuration

### Can multiple people use the same instance?
Currently, it's designed for single-user. For multi-user:
1. Run separate instances with different `.env` files
2. Or build a web interface with authentication
3. Use Docker for isolation

---

## Best Practices

### Should I review posts before publishing?
Initially, yes:
1. Start with `--mode generate-only`
2. Review quality for 1-2 weeks
3. Once satisfied, switch to `--mode auto`

### How often should I post?
Recommended:
- **LinkedIn**: 1-2 times/day
- **Instagram**: 1-3 times/day
- **Facebook**: 1-2 times/day

Quality > Quantity!

### What time should I post?
Default optimal times:
- **LinkedIn**: 9 AM, 12 PM (business hours)
- **Instagram**: 12 PM, 7 PM (lunch and evening)
- **Facebook**: 1 PM, 3 PM (afternoon)

Adjust based on your audience's timezone.

### How do I track performance?
Currently tracks:
- Post history
- Posts per platform
- Posting frequency

For analytics, use platform-native tools:
- LinkedIn Analytics
- Instagram Insights
- Facebook Page Insights

### Should I disclose AI-generated content?
This depends on:
- Your audience expectations
- Platform policies
- Your personal preference

Consider adding a note like "Content crafted with AI assistance"

---

## Security & Privacy

### Is my data secure?
- API keys stored locally in `.env` (gitignored)
- Database stored locally
- No data sent to third parties (except AI/social media APIs)

### Can others see my API keys?
Only if you:
- Commit `.env` to a public repository
- Share your `.env` file
- Give access to your server

Always keep `.env` private!

### What data is collected?
The system stores:
- Generated post text
- Image paths
- Post timestamps
- Platform information

No personal data is collected.

---

## Support & Community

### Where can I get help?
1. Read documentation (README, SETUP_GUIDE, etc.)
2. Check logs in `./logs/`
3. Run `python utils/test_apis.py`
4. Review this FAQ

### How do I report bugs?
Create an issue with:
- Error message
- Steps to reproduce
- Your Python version
- Operating system

### Can I contribute?
Yes! Contributions welcome:
- Bug fixes
- New features
- Documentation improvements
- Platform integrations

### Is there a Discord/Slack community?
Not yet! If there's interest, we can create one.

---

## Roadmap & Future Features

### Planned Features
- [ ] Analytics dashboard
- [ ] A/B testing for posts
- [ ] Video generation
- [ ] More platform support (Twitter, TikTok)
- [ ] Template system
- [ ] Engagement tracking
- [ ] Content calendar
- [ ] Multi-user support

### Can I request features?
Yes! Create an issue describing:
- The feature
- Why it's useful
- How it should work

---

## Miscellaneous

### Can I use this for clients?
Yes, but:
- Each client needs their own credentials
- You're responsible for content quality
- Consider adding terms of service
- Charge appropriately for your service

### Can I sell this as a service?
The code is open source (check LICENSE), but you can:
- Offer it as a managed service
- Build a SaaS on top of it
- White-label for clients

### How is this different from Buffer/Hootsuite?
- **Cost**: $2/month vs $50-200/month
- **AI**: Generates unique content, not just scheduling
- **Open source**: Full control and customization
- **Self-hosted**: Your data, your server

### Will this work in [my country]?
Yes, as long as:
- You can access the AI APIs (Groq, Stability AI)
- Social media platforms are available
- No restrictions on API access

---

Have more questions? Check the documentation or create an issue!
