# 🚀 Deploy to Railway - Step by Step

## ✅ Code Pushed to GitHub Successfully!

Your backend is now at: https://github.com/a6dulhad1/post_generation_python_backend

## 📋 Deploy to Railway (5 Minutes)

### Step 1: Go to Railway
1. Visit https://railway.app
2. Click "Login" (use GitHub account)
3. Click "New Project"

### Step 2: Connect GitHub Repository
1. Click "Deploy from GitHub repo"
2. Select: **a6dulhad1/post_generation_python_backend**
3. Click "Deploy Now"

### Step 3: Configure Environment Variables
After deployment starts, add these environment variables:

Click "Variables" tab and add:

```
GROQ_API_KEY=your_groq_api_key_here
STABILITY_API_KEY=your_stability_api_key_here
PORT=8000
```

**Get your API keys from:**
- **Groq API**: https://console.groq.com/keys
- **Stability AI**: https://platform.stability.ai/account/keys

### Step 4: Wait for Deployment
- Railway will automatically:
  - Install Python dependencies
  - Run the FastAPI server
  - Generate a public URL

### Step 5: Get Your Railway URL
After deployment completes (~2-3 minutes):
1. Click "Settings" tab
2. Under "Networking", click "Generate Domain"
3. Copy your Railway URL (e.g., `https://your-app.up.railway.app`)

### Step 6: Update Flutter App
Update the Flutter app's API URL:

Edit: `flutter_app/lib/config/api_config.dart`
```dart
static const String baseUrl = 'https://your-app.up.railway.app';
```

Replace `your-app.up.railway.app` with your actual Railway domain.

## ✅ Your Backend is Now Live!

Test it by visiting:
- API Docs: `https://your-app.up.railway.app/docs`
- Health Check: `https://your-app.up.railway.app/health`

## 🔧 Railway Configuration Files Created

The following files configure Railway deployment:

### Procfile
```
web: python start.py

```

### runtime.txt
```
python-3.11.0
```

### requirements_api.txt
Contains all Python dependencies

## 📊 What Railway Provides

- ✅ **Automatic HTTPS**
- ✅ **Auto-scaling**
- ✅ **Deployment logs**
- ✅ **Monitoring**
- ✅ **Free tier** (5 services, $5/month credit)
- ✅ **Zero downtime deploys**

## 🎯 After Deployment

### 1. Test Your API
```bash
curl https://your-app.up.railway.app/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "apis": {
    "groq": "operational",
    "stability_ai": "operational"
  }
}
```

### 2. Update Flutter App
```bash
cd flutter_app
# Update api_config.dart with Railway URL
flutter run
```

### 3. Test from Flutter App
- Open app
- Generate ideas
- Chat with AI
- Everything should work with Railway backend!

## 💡 Railway Dashboard Features

### View Logs
1. Go to your Railway project
2. Click "Deployments" tab
3. See real-time logs

### Monitor Usage
1. Click "Metrics" tab
2. See CPU, RAM, bandwidth usage

### Redeploy
1. Push changes to GitHub
2. Railway auto-deploys!
3. Or click "Redeploy" in Railway dashboard

## 🔄 Auto-Deployment

Every time you push to GitHub main branch:
```bash
git add .
git commit -m "Update backend"
git push
```

Railway automatically:
1. Detects the push
2. Builds new image
3. Deploys with zero downtime

## 🐛 Troubleshooting

### Deployment Failed?
Check Railway build logs:
1. Go to Railway project
2. Click "Deployments"
3. View error logs

### Common Issues

#### Missing Dependencies
Add to `requirements_api.txt` and push:
```bash
git add requirements_api.txt
git commit -m "Add missing dependency"
git push
```

#### Environment Variables
Verify in Railway dashboard:
- Settings → Variables
- Make sure GROQ_API_KEY and STABILITY_API_KEY are set

#### Port Issues
Railway uses $PORT environment variable.
Check Procfile has: `--port $PORT`

## 📱 Final Flutter App Configuration

After Railway deployment, update 3 places:

### 1. API Config (Development)
`flutter_app/lib/config/api_config.dart`:
```dart
static const String baseUrl = 'https://your-app.up.railway.app';
```

### 2. For Production Build
Same URL works for:
- Android APK
- iOS IPA
- Web deployment

### 3. No More Local Server Needed!
Your app now uses Railway backend:
- ✅ Available 24/7
- ✅ Accessible from anywhere
- ✅ HTTPS secure
- ✅ No firewall issues

## 🎉 Congratulations!

Your AI Social Media Backend is now:
- ✅ **Live on Railway**
- ✅ **Accessible worldwide**
- ✅ **Auto-deploying from GitHub**
- ✅ **Running with HTTPS**
- ✅ **Monitored and scalable**

## 🔗 Important Links

- **GitHub Repo**: https://github.com/a6dulhad1/post_generation_python_backend
- **Railway Dashboard**: https://railway.app/dashboard
- **Your API** (after deployment): https://your-app.up.railway.app
- **API Docs** (after deployment): https://your-app.up.railway.app/docs

## 💰 Railway Pricing

**Free Tier:**
- $5 free credit per month
- 500 hours execution time
- Perfect for development and testing

**Pro Plan** ($20/month):
- Unlimited projects
- More compute resources
- Priority support

For your app, free tier is enough to start!

---

**Next Steps:**
1. Deploy to Railway (5 minutes)
2. Get your Railway URL
3. Update Flutter app with Railway URL
4. Test the app
5. Share with users!

Your backend is ready for the world! 🌍
