# 🤖 AI Social Media Automation System

> Automate your LinkedIn, Instagram, and Facebook posts with AI-generated content and images.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Fully automated social media posting system that researches trends, generates engaging content, creates AI images, and posts to multiple platforms daily.

---

## ✨ Features

- 🔍 **Trend Research** - Automatically researches current trends in your topics
- ✍️ **AI Content Generation** - Creates unique, engaging posts using Groq AI
- 🎨 **AI Image Generation** - Generates custom images with Stability AI
- 📱 **Multi-Platform Posting** - LinkedIn, Instagram, and Facebook
- 📝 **Custom Prompts** - Post about your achievements with AI enhancement
- 📸 **Screenshot Support** - Upload images to accompany your posts
- 📊 **Post History** - Track all posts in local database
- ⏰ **Automated Scheduling** - Set and forget daily posting
- 🎛️ **Web Dashboard** - View stats and manage content

---

## 📚 Documentation

**New here? Start with these guides:**

| Document | Description | Read Time |
|----------|-------------|-----------|
| **[📖 INDEX.md](INDEX.md)** | Complete documentation index | 2 min |
| **[🚀 QUICK_START.md](QUICK_START.md)** | Get running in 5 minutes | 5 min |
| **[💻 INSTALLATION.md](INSTALLATION.md)** | Platform-specific installation | 10 min |
| **[🔧 SETUP_GUIDE.md](SETUP_GUIDE.md)** | Detailed API configuration | 20 min |
| **[❓ FAQ.md](FAQ.md)** | Frequently asked questions | 15 min |
| **[📊 PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Complete project overview | 10 min |

💡 **Recommended path:** [QUICK_START.md](QUICK_START.md) → [FAQ.md](FAQ.md) → Start using!

---

## 🎯 Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Test
```bash
python utils/test_apis.py
```

### 4. Generate Your First Posts
```bash
python main.py --mode generate-only
```

See [QUICK_START.md](QUICK_START.md) for detailed instructions.

---

## 💰 Cost

| Service | Cost | Purpose |
|---------|------|---------|
| **Groq AI** | FREE | Text generation |
| **Stability AI** | ~$2/month | Image generation |
| **Social Media APIs** | FREE | Posting to platforms |
| **Total** | **~$2/month** | vs $50-200/month for alternatives |

---

## 🎮 Usage Examples

### Fully Automated Daily Posts
```bash
python main.py --mode auto
```

### Post Custom Content with Screenshot
```bash
python main.py --mode manual \
  --prompt "Just closed a $250,000 deal!" \
  --image ./screenshot.png
```

### Generate Ideas Without Posting
```bash
python main.py --mode generate-only --topics "AI,technology,startups"
```

### Start Web Dashboard
```bash
python dashboard.py
# Visit http://localhost:5000
```

### Run Automated Scheduler
```bash
python daily_scheduler.py
```

More examples in [QUICK_START.md](QUICK_START.md#usage-examples)

---

## 📋 Requirements

### Required APIs (Minimum Setup)
- ✅ **Groq API** (FREE) - Text generation
- ✅ **Stability AI** (~$2/month) - Image generation

### Optional APIs (For Posting)
- 📘 **LinkedIn API** (FREE) - Post to LinkedIn
- 📘 **Facebook API** (FREE) - Post to Facebook  
- 📘 **Instagram API** (FREE) - Post to Instagram

### System Requirements
- Python 3.8 or higher
- Internet connection
- ~500MB disk space

Full requirements in [INSTALLATION.md](INSTALLATION.md#prerequisites)

---

## 🏗️ Project Structure

```
├── 📄 Documentation          # All guides and docs
├── ⚙️  Configuration         # .env, requirements.txt
├── 🎯 Main Application       # main.py, dashboard.py
├── 🔧 Services              # AI and content generation
├── 📱 Platforms             # Social media integrations
├── 💾 Database              # Post history tracking
├── 🛠️  Utilities             # Helper functions
└── 📚 Examples              # Usage examples
```

Detailed structure in [INDEX.md](INDEX.md#project-structure)

---

## 🌟 Key Features Explained

### 🤖 Automated Mode
- Researches trends daily
- Generates 3 unique posts
- Creates custom images
- Posts to all platforms
- Zero manual work

### ✍️ Manual Mode
- Provide your own prompt
- AI enhances your message
- Upload screenshots/images
- Review before posting
- Choose specific platforms

### 📊 Generate-Only Mode
- Create content without posting
- Perfect for content planning
- Review and approve later
- Save ideas for future use

See all features in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#key-features)

---

## 🎨 What Gets Generated

For each post, the AI creates:

1. **Trend-Aware Topic** - Based on current trends
2. **Engaging Text** - 150-200 words, platform-optimized
3. **Relevant Hashtags** - 5-10 hashtags per post
4. **Custom Image** - AI-generated visual content
5. **Platform Variants** - Optimized for each platform

Example workflow in [SETUP_GUIDE.md](SETUP_GUIDE.md#example-workflow)

---

## ⚡ Quick Command Reference

```bash
# Installation & Setup
pip install -r requirements.txt
cp .env.example .env

# Test APIs
python utils/test_apis.py

# Generate content (no posting)
python main.py --mode generate-only

# Manual post with custom prompt
python main.py --mode manual --prompt "Your message"

# Automated daily posts
python main.py --mode auto

# Start web dashboard
python dashboard.py

# Run daily scheduler
python daily_scheduler.py

# Windows menu
run_examples.bat

# Linux/Mac menu
./run_examples.sh
```

---

## 🚀 Deployment Options

### Local Development
```bash
python daily_scheduler.py
```

### Docker
```bash
docker-compose up -d
```

### Cloud Deployment
- AWS EC2
- Google Cloud
- DigitalOcean
- Heroku

Deployment guides in [INSTALLATION.md](INSTALLATION.md#deployment)

---

## 📊 Example Use Cases

### 1. E-commerce Business Owner
```bash
python main.py --mode auto --topics "amazon,e-commerce,online-business"
```
**Result:** Daily posts about e-commerce trends

### 2. Sharing Achievements
```bash
python main.py --mode manual \
  --prompt "Hit $250k in sales this month!" \
  --image ./sales-screenshot.png
```
**Result:** Professional post with your screenshot

### 3. Content Planning
```bash
python main.py --mode generate-only
```
**Result:** Week's worth of content ideas to review

More use cases in [FAQ.md](FAQ.md#common-use-cases)

---

## 🛠️ Customization

All aspects are customizable:

- **Content Style** → Edit `services/content_generator.py`
- **Image Style** → Edit `services/image_generator.py`
- **Research Topics** → Edit `.env` file
- **Posting Times** → Edit `daily_scheduler.py`
- **Platforms** → Add to `platforms/` directory

Customization guide in [SETUP_GUIDE.md](SETUP_GUIDE.md#customization)

---

## ❓ Troubleshooting

### Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"API key invalid"**
- Check `.env` file
- No spaces around `=`
- No quotes around values

**"Image generation failed"**
- Check Stability AI credits
- Verify API key

More solutions in [FAQ.md](FAQ.md#troubleshooting)

---

## 📈 Roadmap

- [ ] Analytics dashboard with engagement metrics
- [ ] Video generation support
- [ ] More platforms (Twitter, TikTok)
- [ ] A/B testing for posts
- [ ] Team collaboration features
- [ ] Mobile app

See full roadmap in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#roadmap--future-features)

---

## 🤝 Contributing

Contributions welcome! Whether it's:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🌐 Platform integrations

---

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

- **Groq** for powerful AI text generation
- **Stability AI** for image generation
- **Open source community** for inspiration

---

## 📞 Support

- 📖 Read the [FAQ.md](FAQ.md)
- 🔍 Check [INDEX.md](INDEX.md) for all docs
- 🐛 Report issues on GitHub
- 💬 [Create a discussion]

---

## ⭐ Star History

If you find this helpful, consider giving it a star!

---

**Ready to get started?** 👉 [QUICK_START.md](QUICK_START.md)
