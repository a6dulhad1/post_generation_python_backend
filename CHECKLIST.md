# ✅ Setup Checklist

Use this checklist to track your setup progress.

---

## 📋 Pre-Setup (5 minutes)

- [ ] Python 3.8+ installed
  - Run `python --version` to check
  - If not installed: Visit https://www.python.org/downloads/

- [ ] Git installed (optional)
  - Run `git --version` to check
  - Or download ZIP from repository

- [ ] Text editor ready
  - VS Code, Notepad++, Sublime, or any editor

---

## 🔧 Installation (10 minutes)

- [ ] Download/clone project
  ```bash
  git clone [repository-url]
  cd ai-social-media-automation
  ```

- [ ] Create virtual environment (recommended)
  ```bash
  # Windows
  python -m venv venv
  venv\Scripts\activate
  
  # Mac/Linux
  python3 -m venv venv
  source venv/bin/activate
  ```

- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Create data directories
  ```bash
  # Windows
  mkdir data\images data\generated logs
  
  # Mac/Linux
  mkdir -p data/images data/generated logs
  ```

---

## 🔑 API Keys - Required (15 minutes)

### Groq API (FREE)

- [ ] Visit https://console.groq.com
- [ ] Create free account
- [ ] Navigate to API Keys section
- [ ] Create new API key
- [ ] Copy key (starts with `gsk_`)
- [ ] Save for later ✏️ `_______________________`

### Stability AI (~$2/month)

- [ ] Visit https://platform.stability.ai
- [ ] Create account
- [ ] Add credits ($10 minimum)
- [ ] Go to Account > API Keys
- [ ] Create new API key
- [ ] Copy key (starts with `sk-`)
- [ ] Save for later ✏️ `_______________________`

---

## 📱 Social Media APIs - Optional (30-60 minutes each)

### LinkedIn (Optional)

- [ ] Visit https://www.linkedin.com/developers
- [ ] Create new app
- [ ] Note Client ID ✏️ `_______________________`
- [ ] Note Client Secret ✏️ `_______________________`
- [ ] Set up OAuth redirect URI
- [ ] Request permissions: `w_member_social`, `r_liteprofile`
- [ ] Generate access token
- [ ] Note Access Token ✏️ `_______________________`
- [ ] Test token expiration (60 days)

**Help:** See [SETUP_GUIDE.md](SETUP_GUIDE.md#linkedin-setup)

### Facebook (Optional)

- [ ] Visit https://developers.facebook.com
- [ ] Create new app (Business type)
- [ ] Note App ID ✏️ `_______________________`
- [ ] Note App Secret ✏️ `_______________________`
- [ ] Add Instagram Graph API product
- [ ] Request permissions:
  - [ ] `pages_manage_posts`
  - [ ] `pages_read_engagement`
  - [ ] `instagram_basic`
  - [ ] `instagram_content_publish`
- [ ] Generate access token
- [ ] Convert to long-lived token (60 days)
- [ ] Note Access Token ✏️ `_______________________`

**Help:** See [SETUP_GUIDE.md](SETUP_GUIDE.md#facebook-instagram-setup)

### Instagram (Optional)

- [ ] Ensure Facebook setup complete (above)
- [ ] Connect Instagram Business Account
- [ ] Get Page ID
- [ ] Get Instagram Business Account ID
- [ ] Note IG Account ID ✏️ `_______________________`
- [ ] Test posting permissions

**Help:** See [SETUP_GUIDE.md](SETUP_GUIDE.md#facebook-instagram-setup)

---

## ⚙️ Configuration (5 minutes)

- [ ] Copy environment template
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` file with your keys
  ```
  GROQ_API_KEY=gsk_your_key_here
  STABILITY_AI_API_KEY=sk_your_key_here
  
  # Optional (if you have them)
  LINKEDIN_ACCESS_TOKEN=your_token
  FACEBOOK_ACCESS_TOKEN=your_token
  INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id
  ```

- [ ] Customize settings (optional)
  ```
  POSTS_PER_DAY=3
  RESEARCH_TOPICS=amazon,e-commerce,business,AI
  ```

- [ ] Save and close `.env`

---

## ✅ Verification (5 minutes)

- [ ] Test API connections
  ```bash
  python utils/test_apis.py
  ```

- [ ] Expected results:
  - [ ] ✓ Groq API: Connected
  - [ ] ✓ Stability AI: Connected
  - [ ] ⚠ LinkedIn: (Skip if not configured)
  - [ ] ⚠ Facebook: (Skip if not configured)
  - [ ] ⚠ Instagram: (Skip if not configured)

- [ ] If any errors, check:
  - [ ] API keys are correct in `.env`
  - [ ] No spaces around `=` in `.env`
  - [ ] No quotes around values
  - [ ] Internet connection working

---

## 🎯 First Run (5 minutes)

- [ ] Generate first content (no posting)
  ```bash
  python main.py --mode generate-only
  ```

- [ ] Check output:
  - [ ] Files created in `data/generated/`
  - [ ] Open and review content quality
  - [ ] Check if topics are relevant

- [ ] If content quality is good:
  - [ ] ✓ Ready to proceed!

- [ ] If content needs improvement:
  - [ ] Edit `services/content_generator.py`
  - [ ] Adjust prompts and tone
  - [ ] Run again

---

## 📝 First Manual Post (10 minutes)

- [ ] Prepare your message
  - Example: "Just closed a $250,000 deal!"

- [ ] Run manual mode
  ```bash
  python main.py --mode manual --prompt "Your message"
  ```

- [ ] Review generated content
  - [ ] Text is professional
  - [ ] Hashtags are relevant
  - [ ] Platform choice makes sense

- [ ] Approve and post
  - [ ] Type 'y' when prompted

- [ ] Verify on social media
  - [ ] Check LinkedIn/Instagram/Facebook
  - [ ] Post appeared correctly
  - [ ] Image looks good

---

## 🤖 Enable Automation (Optional)

### Option 1: Python Scheduler

- [ ] Test scheduler
  ```bash
  python daily_scheduler.py --test
  ```

- [ ] If test successful, run daily
  ```bash
  python daily_scheduler.py
  ```

- [ ] Keep terminal open or use:
  ```bash
  # Background (Linux/Mac)
  nohup python daily_scheduler.py &
  ```

### Option 2: Cron (Linux/Mac)

- [ ] Open crontab
  ```bash
  crontab -e
  ```

- [ ] Add line (9 AM daily)
  ```
  0 9 * * * cd /path/to/project && python main.py --mode auto
  ```

- [ ] Save and exit

### Option 3: Task Scheduler (Windows)

- [ ] Open Task Scheduler
- [ ] Create Basic Task
- [ ] Name: "AI Social Media Posts"
- [ ] Trigger: Daily at 9:00 AM
- [ ] Action: Start a program
- [ ] Program: `python.exe`
- [ ] Arguments: `main.py --mode auto`
- [ ] Start in: `C:\path\to\project`
- [ ] Save task

### Option 4: Docker

- [ ] Build image
  ```bash
  docker-compose build
  ```

- [ ] Start services
  ```bash
  docker-compose up -d
  ```

- [ ] Check logs
  ```bash
  docker-compose logs -f
  ```

---

## 🌐 Web Dashboard (Optional)

- [ ] Start dashboard
  ```bash
  python dashboard.py
  ```

- [ ] Open browser
  - [ ] Go to http://localhost:5000

- [ ] Test features:
  - [ ] View statistics
  - [ ] Check post history
  - [ ] Browse recent posts

---

## 📊 Post-Setup Tasks

### Week 1: Testing

- [ ] Review generated content daily
- [ ] Check post quality on platforms
- [ ] Note engagement patterns
- [ ] Adjust topics if needed
- [ ] Fine-tune content style

### Week 2: Optimization

- [ ] Analyze which topics perform best
- [ ] Adjust posting times
- [ ] Customize content tone
- [ ] Add/remove platforms
- [ ] Review hashtag effectiveness

### Week 3: Automation

- [ ] Enable full automation
- [ ] Set up monitoring
- [ ] Schedule token refresh reminders
- [ ] Document any customizations
- [ ] Create backup of `.env` and database

---

## 🔄 Maintenance Schedule

### Daily
- [ ] Check logs for errors
- [ ] Monitor post success rate

### Weekly
- [ ] Review generated content quality
- [ ] Check engagement metrics
- [ ] Adjust topics if needed

### Monthly
- [ ] Review API usage/costs
- [ ] Update token reminders (2 months)
- [ ] Backup database
- [ ] Update dependencies if needed

### Every 60 Days
- [ ] Refresh LinkedIn token
- [ ] Refresh Facebook token
- [ ] Test all integrations

---

## 🆘 Troubleshooting Checklist

If something goes wrong:

- [ ] Check logs in `logs/` directory
- [ ] Run API test: `python utils/test_apis.py`
- [ ] Verify `.env` configuration
- [ ] Check internet connection
- [ ] Review [FAQ.md](FAQ.md) for common issues
- [ ] Check API dashboard for quota/credits
- [ ] Verify tokens haven't expired
- [ ] Try running in verbose mode

---

## 📚 Documentation Checklist

Read these as needed:

- [ ] [README.md](README.md) - Overview
- [ ] [QUICK_START.md](QUICK_START.md) - 5-min guide
- [ ] [INSTALLATION.md](INSTALLATION.md) - Detailed install
- [ ] [SETUP_GUIDE.md](SETUP_GUIDE.md) - API setup
- [ ] [FAQ.md](FAQ.md) - Common questions
- [ ] [WORKFLOW.md](WORKFLOW.md) - How it works
- [ ] [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Full details

---

## ✨ Optional Enhancements

Once comfortable:

- [ ] Customize image styles
- [ ] Add custom templates
- [ ] Set up analytics tracking
- [ ] Create brand voice guidelines
- [ ] Add more platforms
- [ ] Build team workflows
- [ ] Implement A/B testing
- [ ] Add engagement tracking

---

## 🎉 You're Done!

Congratulations! Your AI Social Media Automation System is ready.

**Next Steps:**
1. Start with generate-only mode
2. Review and approve content
3. Gradually enable automation
4. Monitor and optimize

**Need Help?**
- Check [FAQ.md](FAQ.md)
- Review [INDEX.md](INDEX.md) for all docs
- Run `python utils/test_apis.py`

**Happy Automating! 🚀**

---

## 📝 Notes Section

Use this space for your own notes:

```
Setup Date: _____________________

API Keys Obtained:
- Groq: ☐
- Stability AI: ☐
- LinkedIn: ☐
- Facebook: ☐
- Instagram: ☐

Custom Configurations:
_____________________________________
_____________________________________
_____________________________________

Token Refresh Dates:
- LinkedIn: _____________________
- Facebook: _____________________

Issues Encountered:
_____________________________________
_____________________________________
_____________________________________

Solutions/Workarounds:
_____________________________________
_____________________________________
_____________________________________
```
