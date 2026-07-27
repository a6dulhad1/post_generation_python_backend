# 📊 System Workflow

Visual guide to how the AI Social Media Automation System works.

---

## 🔄 Main Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER TRIGGERS SYSTEM                      │
│  (python main.py --mode auto/manual/generate-only)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   LOAD CONFIGURATION                         │
│  • Read .env file                                            │
│  • Validate API keys                                         │
│  • Load settings (topics, platforms, posts per day)          │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬──────────────┐
        │                         │              │
        ▼                         ▼              ▼
   AUTO MODE               MANUAL MODE      GENERATE-ONLY
        │                         │              │
        │                         │              │
        ▼                         ▼              ▼
```

---

## 🤖 Auto Mode Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    1. TREND RESEARCH                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Groq AI analyzes current trends                   │   │
│  │  • Topics: From RESEARCH_TOPICS in .env              │   │
│  │  • Generates 3 post ideas with:                      │   │
│  │    - Topic/Theme                                      │   │
│  │    - Angle (why it's interesting)                    │   │
│  │    - Key points                                       │   │
│  │    - Target audience                                  │   │
│  │    - Best platform                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 2. CONTENT GENERATION                        │
│  For each post idea:                                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Groq AI generates:                                 │   │
│  │    - Post text (150-200 words)                       │   │
│  │    - 5-10 relevant hashtags                          │   │
│  │    - Detailed image description                      │   │
│  │  • Platform-optimized:                                │   │
│  │    - LinkedIn: Professional tone                     │   │
│  │    - Instagram: Visual, emoji-friendly               │   │
│  │    - Facebook: Community-focused                     │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  3. IMAGE GENERATION                         │
│  For each post:                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Stability AI creates image from description        │   │
│  │  • Base size: 1024x1024 pixels                       │   │
│  │  • Style: Professional by default                    │   │
│  │  • Saves to: data/images/post_N_platform.png         │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                4. PLATFORM OPTIMIZATION                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Resize images for each platform:                  │   │
│  │    - LinkedIn: 1200x627                              │   │
│  │    - Instagram: 1080x1080                            │   │
│  │    - Facebook: 1200x630                              │   │
│  │  • Adjust content formatting                         │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    5. POST TO PLATFORMS                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Upload image to platform                          │   │
│  │  • Create post with text + hashtags                  │   │
│  │  • Verify successful posting                         │   │
│  │  • Handle errors gracefully                          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   6. SAVE TO DATABASE                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Record post in SQLite database                    │   │
│  │  • Store: text, hashtags, image path, timestamp      │   │
│  │  • Track: platform, status, post ID                  │   │
│  │  • Use for: duplicate checking, analytics            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
                   DONE ✓
```

---

## ✍️ Manual Mode Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                                │
│  • Custom prompt (e.g., "Just closed a $250k deal!")        │
│  • Optional image/screenshot                                 │
│  • Optional context/details                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              GROQ AI ANALYZES PROMPT                         │
│  • Understands user intent                                   │
│  • Identifies key message                                    │
│  • Determines best platform                                  │
│  • Creates structured post idea                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           GROQ AI GENERATES PROFESSIONAL CONTENT             │
│  • Enhances user's message                                   │
│  • Adds professional tone                                    │
│  • Creates engaging copy                                     │
│  • Generates relevant hashtags                               │
│  • Suggests image if not provided                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
            ┌────────┴─────────┐
            │                  │
    User provided image?      No
            │                  │
           Yes                 ▼
            │          ┌───────────────┐
            │          │ Generate image│
            │          │ with Stability│
            │          │      AI       │
            │          └───────┬───────┘
            │                  │
            └──────────┬───────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   PREVIEW TO USER                            │
│  ╔═══════════════════════════════════════════════════════╗  │
│  ║  Platform: LinkedIn                                   ║  │
│  ║  Topic: Major Business Milestone                      ║  │
│  ║                                                         ║  │
│  ║  Just secured a $250,000 deal with a Fortune 500...  ║  │
│  ║  This milestone represents months of hard work...     ║  │
│  ║                                                         ║  │
│  ║  #BusinessGrowth #Milestone #B2B #Success            ║  │
│  ║                                                         ║  │
│  ║  Image: screenshot_enhanced.png                       ║  │
│  ╚═══════════════════════════════════════════════════════╝  │
│                                                              │
│  Do you want to post this? (Y/n)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
            ┌────────┴─────────┐
            │                  │
           Yes                No
            │                  │
            ▼                  ▼
    ┌──────────────┐    ┌──────────┐
    │ Post to      │    │ Cancelled│
    │ platform(s)  │    └──────────┘
    └──────┬───────┘
           │
           ▼
    Save to database
           │
           ▼
        DONE ✓
```

---

## 📝 Generate-Only Mode Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH TRENDS                           │
│  • Same as Auto Mode                                         │
│  • Generates 3 post ideas                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  GENERATE CONTENT                            │
│  • Creates text for each idea                                │
│  • Generates hashtags                                        │
│  • Creates image prompts                                     │
│  • NO images generated (saves credits)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  SAVE TO FILES                               │
│  • data/generated/idea_1.txt                                 │
│  • data/generated/idea_2.txt                                 │
│  • data/generated/idea_3.txt                                 │
│                                                              │
│  Each file contains:                                         │
│  - Topic                                                     │
│  - Platform recommendation                                   │
│  - Full post text                                            │
│  - Hashtags                                                  │
│  - Image description                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 DISPLAY SUMMARY                              │
│  ╔═══════════════════════════════════════════════════════╗  │
│  ║  Generated 3 Post Ideas                                ║  │
│  ║                                                         ║  │
│  ║  1. Topic: Amazon's Q4 Strategy                       ║  │
│  ║     Platform: LinkedIn                                 ║  │
│  ║     Saved to: data/generated/idea_1.txt               ║  │
│  ║                                                         ║  │
│  ║  2. Topic: E-commerce Holiday Trends                  ║  │
│  ║     Platform: Instagram                                ║  │
│  ║     Saved to: data/generated/idea_2.txt               ║  │
│  ║                                                         ║  │
│  ║  3. Topic: Small Business Success Stories             ║  │
│  ║     Platform: Facebook                                 ║  │
│  ║     Saved to: data/generated/idea_3.txt               ║  │
│  ╚═══════════════════════════════════════════════════════╝  │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
                   DONE ✓
           (NO posting performed)
```

---

## 🔁 Daily Scheduler Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              DAILY SCHEDULER STARTS                          │
│  • Loads schedule from daily_scheduler.py                    │
│  • Configured times: 9:00 AM, 3:00 PM (default)             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │ Wait for next  │
            │ scheduled time │
            └────────┬───────┘
                     │
                     ▼
            Time reached (e.g., 9:00 AM)
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                EXECUTE AUTO MODE                             │
│  • Runs: python main.py --mode auto                          │
│  • Generates posts                                           │
│  • Posts to platforms                                        │
│  • Logs results                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │ Log completion │
            │ Go back to wait│
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ Next scheduled │
            │ time (3:00 PM) │
            └────────┬───────┘
                     │
                     ▼
                   REPEAT
```

---

## 🌐 Web Dashboard Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              USER OPENS BROWSER                              │
│  • Navigate to http://localhost:5000                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              DASHBOARD LOADS                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Statistics Panel:                                    │   │
│  │  • Total posts: 45                                    │   │
│  │  • This week: 12                                      │   │
│  │  • By platform: LinkedIn(20), Instagram(15)...       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Recent Posts:                                        │   │
│  │  • Post 1: [LinkedIn] "AI in e-commerce..."          │   │
│  │  • Post 2: [Instagram] "Holiday marketing tips..."   │   │
│  │  • Post 3: [Facebook] "Small business success..."    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
            User Interacts
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌─────────────┐ ┌─────────┐ ┌─────────────┐
│View history │ │Generate │ │View images  │
│ by date     │ │new idea │ │             │
└─────────────┘ └─────────┘ └─────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│   USER   │────────▶│ MAIN.PY  │◀───────│  .ENV    │
└──────────┘         └────┬─────┘         └──────────┘
                          │
                ┌─────────┼─────────┐
                │                   │
                ▼                   ▼
        ┌───────────────┐   ┌──────────────┐
        │  GROQ API     │   │ STABILITY AI │
        │ (Text/Ideas)  │   │   (Images)   │
        └───────┬───────┘   └──────┬───────┘
                │                   │
                └─────────┬─────────┘
                          │
                          ▼
                ┌─────────────────┐
                │  POST SCHEDULER │
                └────────┬────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│   LINKEDIN   │ │  INSTAGRAM  │ │   FACEBOOK   │
└──────────────┘ └─────────────┘ └──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                ┌────────────────┐
                │   DATABASE     │
                │  (Post History)│
                └────────────────┘
```

---

## 📊 Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                      MAIN APPLICATION                        │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐          │
│  │   CONFIG   │  │  SERVICES  │  │  PLATFORMS  │          │
│  │            │  │            │  │             │          │
│  │ settings.py│─▶│ trend_res. │─▶│ linkedin.py │          │
│  │  .env      │  │ content_g. │  │ instagram.py│          │
│  └────────────┘  │ image_gen. │  │ facebook.py │          │
│                  │ scheduler  │  └─────────────┘          │
│                  └────────────┘                             │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐          │
│  │  DATABASE  │◀─│   UTILS    │  │  EXTERNAL   │          │
│  │            │  │            │  │             │          │
│  │post_history│  │ helpers.py │  │  Groq API   │          │
│  │            │  │ test_apis  │  │Stability AI │          │
│  └────────────┘  └────────────┘  └─────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Decision Flow

```
START
  │
  ▼
Load .env and validate
  │
  ├─ All required keys present? ─No─▶ ERROR: Configure .env
  │                               
 Yes
  │
  ▼
Parse command line arguments
  │
  ├─ Mode = auto? ──Yes─▶ Run Auto Workflow
  │                 
  ├─ Mode = manual? ─Yes─▶ Run Manual Workflow
  │
  └─ Mode = generate? ─Yes─▶ Run Generate-Only
                              
                              │
                              ▼
                        Check platform APIs
                              │
                    ├─ APIs configured? ─Yes─▶ Post to platforms
                    │                   
                   No
                    │
                    ▼
                Mock post (show what would be posted)
                    │
                    ▼
                Save to database
                    │
                    ▼
                  DONE ✓
```

---

## 📈 Error Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    OPERATION STARTS                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
              Try to execute
                     │
            ┌────────┴────────┐
            │                 │
       Succeeds          Error occurs
            │                 │
            ▼                 ▼
    Continue to next   ┌──────────────┐
       operation       │ Log error    │
                       │ to logs/     │
                       └──────┬───────┘
                              │
                   ┌──────────┴──────────┐
                   │                     │
              Recoverable?            Fatal?
                   │                     │
                  Yes                   No
                   │                     │
                   ▼                     ▼
           Retry with      ┌──────────────────┐
           backoff         │ Notify user      │
                          │ Exit gracefully  │
                          └──────────────────┘
```

---

## 🔐 Security Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    API KEY HANDLING                          │
│                                                              │
│  .env file (gitignored)                                      │
│     │                                                        │
│     ▼                                                        │
│  Loaded by settings.py                                       │
│     │                                                        │
│     ▼                                                        │
│  Validated on startup                                        │
│     │                                                        │
│     ▼                                                        │
│  Used in API calls (never logged)                            │
│     │                                                        │
│     ▼                                                        │
│  Transmitted over HTTPS only                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

For more details, see:
- [QUICK_START.md](QUICK_START.md) - Getting started
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Configuration details
- [FAQ.md](FAQ.md) - Common questions
- [INDEX.md](INDEX.md) - All documentation
