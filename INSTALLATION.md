# Installation Guide

Complete installation instructions for all platforms.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+** (3.11 recommended)
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

If you don't have Python installed:
- **Windows**: https://www.python.org/downloads/
- **Mac**: `brew install python` or https://www.python.org/downloads/
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

---

## Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Clone or Download
```bash
# Option A: Clone with Git
git clone https://github.com/yourusername/ai-social-media-automation.git
cd ai-social-media-automation

# Option B: Download ZIP
# Download and extract the ZIP file, then navigate to the folder
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment
```bash
# Copy example config
cp .env.example .env

# Edit .env with your API keys
# Windows: notepad .env
# Mac/Linux: nano .env or vim .env
```

#### Step 5: Create Directories
```bash
# Windows
mkdir data\images data\generated logs

# Mac/Linux
mkdir -p data/images data/generated logs
```

#### Step 6: Test Installation
```bash
python utils/test_apis.py
```

---

### Method 2: Docker Installation

#### Prerequisites
- Docker Desktop installed
- Docker Compose installed

#### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/ai-social-media-automation.git
cd ai-social-media-automation
```

#### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

#### Step 3: Build and Run
```bash
# Build the image
docker-compose build

# Run the scheduler
docker-compose up -d social-media-bot

# Run the dashboard
docker-compose up -d dashboard

# View logs
docker-compose logs -f
```

#### Step 4: Stop Services
```bash
docker-compose down
```

---

## Platform-Specific Instructions

### Windows

#### Installing Python
1. Download from https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Verify: `python --version`

#### Installing Dependencies
```cmd
# Open Command Prompt or PowerShell
cd path\to\project

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Running the Application
```cmd
# Test APIs
python utils\test_apis.py

# Generate ideas
python main.py --mode generate-only

# Use the batch script
run_examples.bat
```

#### Scheduling (Windows Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Name: "AI Social Media Posts"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
   - Program: `C:\path\to\python.exe`
   - Arguments: `main.py --mode auto`
   - Start in: `C:\path\to\project`

---

### macOS

#### Installing Python
```bash
# Using Homebrew (recommended)
brew install python

# Or download from https://www.python.org/downloads/
```

#### Installing Dependencies
```bash
cd /path/to/project

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Running the Application
```bash
# Make scripts executable
chmod +x run_examples.sh

# Test APIs
python utils/test_apis.py

# Generate ideas
python main.py --mode generate-only

# Use the shell script
./run_examples.sh
```

#### Scheduling (Cron)
```bash
# Edit crontab
crontab -e

# Add this line for daily posts at 9 AM
0 9 * * * cd /path/to/project && /path/to/project/venv/bin/python main.py --mode auto >> /path/to/project/logs/cron.log 2>&1
```

---

### Linux (Ubuntu/Debian)

#### Installing Python
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Installing Dependencies
```bash
cd /path/to/project

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Running the Application
```bash
# Make scripts executable
chmod +x run_examples.sh

# Test APIs
python utils/test_apis.py

# Generate ideas
python main.py --mode generate-only

# Use the shell script
./run_examples.sh
```

#### Scheduling (Systemd Service)
Create `/etc/systemd/system/social-media-bot.service`:
```ini
[Unit]
Description=AI Social Media Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/python daily_scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable social-media-bot
sudo systemctl start social-media-bot
sudo systemctl status social-media-bot
```

---

## Verification

### 1. Test API Connections
```bash
python utils/test_apis.py
```

Expected output:
```
✓ Groq API: Connected successfully
✓ Stability AI: Connected successfully
⚠ LinkedIn API: No access token configured (skipping)
⚠ Facebook API: No access token configured (skipping)
⚠ Instagram API: No credentials configured (skipping)
```

### 2. Generate Test Content
```bash
python main.py --mode generate-only --topics "test"
```

Check `./data/generated/` for output files.

### 3. Run Examples
```bash
python examples/example_usage.py
```

---

## Troubleshooting

### Common Issues

#### "Python not found" or "python is not recognized"
**Solution**: 
- Windows: Add Python to PATH or use full path: `C:\Python311\python.exe`
- Mac/Linux: Use `python3` instead of `python`

#### "pip: command not found"
**Solution**:
```bash
# Windows
python -m pip install -r requirements.txt

# Mac/Linux
python3 -m pip install -r requirements.txt
```

#### "Permission denied" (Mac/Linux)
**Solution**:
```bash
chmod +x run_examples.sh
# or
sudo python main.py --mode auto
```

#### "Module not found" errors
**Solution**:
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install --upgrade -r requirements.txt
```

#### "API Key Invalid"
**Solution**:
- Check `.env` file has correct keys
- No spaces around `=` in `.env`
- Keys should not have quotes
- Verify keys are active in respective dashboards

#### "Image generation failed"
**Solution**:
- Check Stability AI credits
- Verify API key is correct
- Check internet connection
- Try reducing image size (width/height)

#### "Access token expired"
**Solution**:
- LinkedIn tokens expire after 60 days
- Facebook tokens expire after 60 days
- Generate new tokens from respective platforms

#### Import errors with Flask (Dashboard)
**Solution**:
```bash
pip install flask>=3.0.0
```

---

## Development Setup

### Installing Development Dependencies
```bash
# Install with development extras
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
```

### Type Checking
```bash
mypy .
```

---

## Uninstallation

### Standard Installation
```bash
# Deactivate virtual environment
deactivate

# Remove project directory
rm -rf /path/to/project

# Or on Windows
rmdir /s /q C:\path\to\project
```

### Docker Installation
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes
docker-compose down -v
```

---

## Getting Help

If you encounter issues:

1. **Check logs**: `./logs/` directory
2. **Run diagnostics**: `python utils/test_apis.py`
3. **Review documentation**: `README.md`, `SETUP_GUIDE.md`
4. **Check Python version**: `python --version` (should be 3.8+)
5. **Verify dependencies**: `pip list`

---

## Next Steps

After successful installation:

1. Read `QUICK_START.md` for 5-minute setup
2. Read `SETUP_GUIDE.md` for detailed configuration
3. Run `python examples/example_usage.py` to see examples
4. Configure your API keys in `.env`
5. Start with `--mode generate-only` to test
