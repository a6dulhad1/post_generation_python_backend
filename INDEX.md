# 📚 Documentation Index

Complete guide to the AI Social Media Automation System.

---

## 🚀 Getting Started

Start here if you're new to the project:

1. **[README.md](README.md)** - Project overview and features
2. **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
3. **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation for all platforms
4. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete API configuration guide

**Recommended path for beginners:**
```
README.md → QUICK_START.md → FAQ.md → Start using!
```

---

## 📖 Core Documentation

### Project Information
- **[README.md](README.md)** - Main project documentation
  - What the project does
  - Key features
  - Requirements overview
  - Basic usage examples

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive summary
  - Complete requirements checklist
  - Project structure
  - Cost breakdown
  - Use cases
  - What makes it different

---

## 🔧 Setup & Installation

### Installation Guides
- **[INSTALLATION.md](INSTALLATION.md)** - Platform-specific installation
  - Windows setup
  - macOS setup
  - Linux setup
  - Docker installation
  - Troubleshooting installation issues

- **[QUICK_START.md](QUICK_START.md)** - Fast setup (5 minutes)
  - Minimum configuration
  - First run instructions
  - Basic usage examples
  - Quick troubleshooting

### Configuration
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - API configuration
  - Getting Groq API key
  - Setting up Stability AI
  - LinkedIn OAuth flow
  - Facebook/Instagram setup
  - Access token management
  - Advanced configuration

---

## 💡 Usage & Examples

### Running the Application
- **Command Line Usage** (see [README.md](README.md))
  - Auto mode (fully automated)
  - Manual mode (custom prompts)
  - Generate-only mode (no posting)
  
- **Example Scripts**
  - `examples/example_usage.py` - Interactive examples
  - `run_examples.bat` - Windows menu system
  - `run_examples.sh` - Linux/Mac menu system

### Common Tasks
```bash
# Test APIs
python utils/test_apis.py

# Generate ideas only
python main.py --mode generate-only

# Post with custom prompt
python main.py --mode manual --prompt "Your message"

# Automated daily posts
python main.py --mode auto

# Start web dashboard
python dashboard.py
```

---

## ❓ Help & Support

- **[FAQ.md](FAQ.md)** - Frequently asked questions
  - General questions
  - Technical questions
  - API & credentials
  - Features & usage
  - Content quality
  - Troubleshooting
  - Advanced usage
  - Best practices

---

## 📁 Project Structure

```
├── 📄 Documentation
│   ├── README.md              # Main documentation
│   ├── INDEX.md               # This file
│   ├── QUICK_START.md         # 5-minute guide
│   ├── INSTALLATION.md        # Installation guide
│   ├── SETUP_GUIDE.md         # API setup guide
│   ├── PROJECT_SUMMARY.md     # Project summary
│   └── FAQ.md                 # FAQ
│
├── ⚙️ Configuration
│   ├── .env.example           # Environment variables template
│   ├── .gitignore             # Git ignore rules
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Docker configuration
│   └── docker-compose.yml     # Docker Compose config
│
├── 🎯 Main Application
│   ├── main.py                # Entry point
│   ├── daily_scheduler.py     # Daily automation
│   └── dashboard.py           # Web dashboard
│
├── 🔧 Core Services
│   ├── config/
│   │   └── settings.py        # Configuration management
│   ├── services/
│   │   ├── trend_research.py      # Trend research
│   │   ├── content_generator.py   # Content generation
│   │   ├── image_generator.py     # Image generation
│   │   └── post_scheduler.py      # Post scheduling
│   ├── platforms/
│   │   ├── linkedin.py        # LinkedIn integration
│   │   ├── instagram.py       # Instagram integration
│   │   └── facebook.py        # Facebook integration
│   ├── database/
│   │   └── post_history.py    # Post history tracking
│   └── utils/
│       ├── helpers.py         # Utility functions
│       └── test_apis.py       # API testing
│
├── 📚 Examples
│   └── examples/
│       └── example_usage.py   # Usage examples
│
└── 🚀 Run Scripts
    ├── run_examples.bat       # Windows launcher
    └── run_examples.sh        # Linux/Mac launcher
```

---

## 🎓 Learning Path

### For Beginners
1. Read [README.md](README.md) - Understand what it does
2. Follow [QUICK_START.md](QUICK_START.md) - Get it running
3. Check [FAQ.md](FAQ.md) - Common questions
4. Experiment with generate-only mode
5. Try manual posts
6. Configure social media APIs
7. Enable automation

### For Developers
1. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Architecture overview
2. Review code structure in `services/` and `platforms/`
3. Understand the database schema in `database/post_history.py`
4. Customize prompts in `services/content_generator.py`
5. Add new platforms by following existing patterns
6. Contribute improvements!

### For Business Users
1. Read [README.md](README.md) - Features and benefits
2. Review cost breakdown in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup
4. Start with generate-only mode
5. Review content quality
6. Gradually enable automation
7. Monitor engagement and adjust

---

## 🔍 Quick Reference

### API Keys Required
| Service | Cost | Purpose | Guide |
|---------|------|---------|-------|
| Groq | FREE | Text generation | [SETUP_GUIDE.md](SETUP_GUIDE.md#groq-api) |
| Stability AI | ~$2/mo | Image generation | [SETUP_GUIDE.md](SETUP_GUIDE.md#stability-ai) |
| LinkedIn | FREE | Post to LinkedIn | [SETUP_GUIDE.md](SETUP_GUIDE.md#linkedin-setup) |
| Facebook | FREE | Post to Facebook | [SETUP_GUIDE.md](SETUP_GUIDE.md#facebook-instagram-setup) |
| Instagram | FREE | Post to Instagram | [SETUP_GUIDE.md](SETUP_GUIDE.md#facebook-instagram-setup) |

### Command Quick Reference
```bash
# Installation
pip install -r requirements.txt
cp .env.example .env

# Testing
python utils/test_apis.py

# Usage Modes
python main.py --mode generate-only
python main.py --mode manual --prompt "Message"
python main.py --mode auto

# Dashboard
python dashboard.py

# Scheduler
python daily_scheduler.py
```

### File Quick Reference
| Need to... | Edit this file |
|------------|----------------|
| Change API keys | `.env` |
| Customize content style | `services/content_generator.py` |
| Adjust posting times | `daily_scheduler.py` |
| Add new platform | Create `platforms/your_platform.py` |
| Change topics | `.env` (RESEARCH_TOPICS) |
| Modify image style | `services/image_generator.py` |

---

## 🛠️ Troubleshooting Guide

### Common Issues
| Problem | Solution | Documentation |
|---------|----------|---------------|
| Installation errors | Check [INSTALLATION.md](INSTALLATION.md#troubleshooting) | Troubleshooting section |
| API connection issues | Run `python utils/test_apis.py` | [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) |
| Content quality concerns | Review [FAQ.md](FAQ.md#content-quality) | Content Quality section |
| Token expired | See [FAQ.md](FAQ.md#how-long-do-access-tokens-last) | API & Credentials |
| Platform posting fails | Check [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) | Platform-specific guides |

---

## 📊 Features by Mode

### Auto Mode
- ✅ Automated trend research
- ✅ Generates 3 posts per day
- ✅ AI images
- ✅ Posts to all platforms
- ✅ No manual intervention

**Use when:** You want fully automated posting

### Manual Mode
- ✅ Your custom prompt
- ✅ Optional image upload
- ✅ AI enhances your message
- ✅ Review before posting
- ✅ Choose platforms

**Use when:** You have specific content to share

### Generate-Only Mode
- ✅ Generates ideas and content
- ✅ No posting
- ✅ Saves to files
- ✅ Review and approve later

**Use when:** Planning content or testing quality

---

## 🎯 Use Case Examples

### E-commerce Business
- **Goal:** Daily posts about Amazon/e-commerce trends
- **Setup:** Auto mode with topics "amazon,e-commerce,online-business"
- **Frequency:** 2-3 posts/day
- **Guide:** [QUICK_START.md](QUICK_START.md#common-use-cases)

### Achievement Sharing
- **Goal:** Share business milestones with screenshots
- **Setup:** Manual mode with custom prompts
- **Example:** "$250k order" with screenshot
- **Guide:** [FAQ.md](FAQ.md#can-i-post-a-screenshot-with-context)

### Content Planning
- **Goal:** Generate ideas for the week
- **Setup:** Generate-only mode
- **Review:** Edit and schedule manually
- **Guide:** [README.md](README.md#usage)

---

## 🔗 External Resources

### API Documentation
- [Groq API Docs](https://console.groq.com/docs)
- [Stability AI Docs](https://platform.stability.ai/docs)
- [LinkedIn API](https://docs.microsoft.com/linkedin/)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram API](https://developers.facebook.com/docs/instagram-api)

### Tools & Services
- [Python.org](https://www.python.org/) - Python downloads
- [Docker](https://www.docker.com/) - Containerization
- [Git](https://git-scm.com/) - Version control

---

## 📝 Contributing

Want to improve the project?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#roadmap--future-features) for planned features.

---

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

- Groq for powerful AI text generation
- Stability AI for image generation
- Open source community

---

**Need help?** Start with [FAQ.md](FAQ.md) or check the relevant guide above!

**First time here?** Go to [QUICK_START.md](QUICK_START.md) for a 5-minute setup!

**Ready to deploy?** Check [INSTALLATION.md](INSTALLATION.md) for your platform!
