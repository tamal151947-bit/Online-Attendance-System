# ⚠️ Render Free Tier Limitation

## Face Recognition Disabled

The face-recognition library with dlib **cannot be deployed on Render's free tier** due to:
- **Build memory limit**: Compiling dlib requires >8GB RAM, free tier has much less
- **Build time limit**: Compilation takes too long for free tier timeouts

## Current Deployment

This deployment works **WITHOUT face recognition features**:
- ✅ Student registration (manual  entry)
- ✅ Attendance tracking (manual)
- ✅ Reports and dashboard
- ✅ MongoDB Atlas cloud storage
- ❌ Face recognition attendance (disabled)

## To Enable Face Recognition

### Option 1: Upgrade to Render Paid Tier ($7/month)
- Paid tier has enough build memory for dlib compilation
- Add back to requirements.txt:
  ```
  numpy==1.24.3
  opencv-python-headless==4.8.0.76
  dlib==19.24.0
  face-recognition==1.3.0
  ```

### Option 2: Use Docker Deployment
- Build locally with pre-compiled dependencies
- Deploy as Docker container
- More complex but works on free tier

### Option 3: Alternative Platform
- **Heroku** (paid:$5/month, buildpack available)
- **Railway** (generous free tier, but still may have issues)
- **PythonAnywhere** (easier for Python, $5/month)
- **AWS EC2 / DigitalOcean** (full control, $4-5/month)

### Option 4: Use Alternative Library
- Replace face-recognition with **DeepFace** or **InsightFace**
- Some have pre-built wheels
- Different API, requires code changes

## Testing Locally

Face recognition works fine locally:
```bash
pip install -r requirements-full.txt  # Create this with face-recognition deps
python app.py
```

## Recommended Action

For production with face-recognition:
1. **Best**: Upgrade to Render paid tier ($7/month) - simplest solution
2. **Alternative**: Deploy to PythonAnywhere ($5/month) - Python-optimized
3. **Advanced**: Use Docker with pre-built dlib wheel

For now, the app is deployed **without face recognition** but all other features work!
