# 🚀 Render Deployment Guide

## ✅ Fixed Issues

Your application has been configured for Render deployment with the following fixes:

1. **opencv-python** → **opencv-python-headless** (no GUI dependencies)
2. Added **gunicorn** as production WSGI server
3. Added **cmake** and **dlib** explicitly to requirements
4. Updated app to use **PORT** environment variable from Render
5. Created **build.sh** script for system dependencies
6. Created **render.yaml** for automatic deployment configuration
7. Added **runtime.txt** to specify Python version

## 📋 Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Configure for Render deployment"
   git push
   ```

2. **Create New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml` and configure everything

3. **Set Environment Variables**
   - In Render dashboard, go to your service
   - Navigate to **Environment** tab
   - Add: `MONGODB_URI` = (your MongoDB Atlas connection string)
   - `SECRET_KEY` should be auto-generated

4. **Deploy!**
   - Click **"Create Web Service"**
   - Wait for build to complete (5-10 minutes for face-recognition)

### Option 2: Manual Setup

1. Create New Web Service on Render
2. Configure:
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11.0
3. Add environment variables (MONGODB_URI, SECRET_KEY)
4. Deploy

## ⚠️ Important Notes

### Build Time
- First deployment takes **5-10 minutes** due to face-recognition dependencies (dlib compilation)
- Subsequent deployments are faster with Render's caching

### MongoDB Atlas
- Ensure your MongoDB Atlas cluster allows connections from **0.0.0.0/0**
- Or add Render's IP addresses to IP whitelist
- Get MONGODB_URI from Atlas dashboard (Connect → Drivers)

### Free Tier Limitations
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Upgrade to paid tier for 24/7 uptime

## 🔍 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Common issue: dlib compilation timeout → upgrade to paid tier for more build time

### App Won't Start
- Verify MONGODB_URI is set correctly
- Check if MongoDB Atlas IP whitelist includes Render
- Review deployment logs for Python errors

### Face Recognition Not Working
- Ensure opencv-python-headless is installed (not opencv-python)
- Check if image sizes are reasonable (large images may timeout)

## 🧪  Testing Locally with Gunicorn

Before deploying, test with gunicorn locally:

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Test with gunicorn
gunicorn app:app
```

Access at http://localhost:8000

## 📊 Monitoring

After deployment:
- Check **Logs** tab in Render dashboard for runtime errors
- Monitor **Metrics** for performance
- Set up **Health Checks** in render.yaml (already configured)

## 🎯 Next Steps

1. Push code to GitHub
2. Deploy on Render
3. Configure MongoDB Atlas IP whitelist
4. Test face recognition functionality
5. Consider upgrading to paid tier if build times are too long

## 🆘 Need Help?

Common errors and solutions:
- **"ModuleNotFoundError: No module named 'cv2'"** → opencv-python-headless issue, rebuild
- **"Cannot connect to MongoDB"** → Check MONGODB_URI and Atlas IP whitelist
- **"Build timeout"** → face-recognition compilation, needs paid tier or simpler alternative
- **"Port already in use"** → Render manages ports automatically, ensure app uses `os.getenv('PORT')`

Good luck! 🚀
