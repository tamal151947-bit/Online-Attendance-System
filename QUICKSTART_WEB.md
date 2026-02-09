# 🚀 Quick Start Guide - Web Version

Get your Face Recognition Attendance System running in 2 minutes!

## Prerequisites Check

✅ Python 3.7+ installed
✅ Virtual environment activated (.venv folder exists)
✅ Browser with camera access
✅ Windows/Mac/Linux system

## Installation (2 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected output**: Successfully installed flask, flask-sqlalchemy, opencv-python, face-recognition, etc.

**Troubleshooting**:
- If pip not found: Use `python -m pip` instead
- If permission denied: Run as Administrator
- If packages fail: Check internet connection

### Step 2: Start the Server
```bash
python app.py
```

**Expected output**:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * WARNING: This is a development server...
Press CTRL+C to stop the server
```

## Access the Application

### In your web browser, go to:
```
http://localhost:5000
```

**If it doesn't load:**
- Wait 5-10 seconds for server startup
- Refresh the page (F5)
- Try http://127.0.0.1:5000 instead
- Check if port 5000 is in use: Change in app.py line: `app.run(port=5001)`

## First Time Setup (3 Steps)

### Step 1: Go to Admin Panel
Click **"⚙️ Admin Panel"** in the sidebar

### Step 2: Add Your First Student
1. Enter name: "Test Student"
2. Enter roll: "001"
3. Upload a clear photo of your face
4. Click **"Add Student"**
5. Wait for confirmation

### Step 3: Mark Attendance
1. Click **"📷 Mark Attendance"**
2. Click **"Start Camera"**
3. Allow camera access when prompted
4. Click **"Mark Attendance"**
5. See your name appear in the marked list!

## Navigation Guide

| Button | Purpose | Action |
|--------|---------|--------|
| 📊 Dashboard | View statistics | Main landing page |
| ⚙️ Admin Panel | Manage students | Add/delete students |
| 📷 Mark Attendance | Face recognition | Record attendance |
| 📈 Reports | View records | See who's present |

## Common Issues & Quick Fixes

### "Webcam not working"
```bash
✓ Go to admin panel and test with admin.html first
✓ Check browser security: Chrome/Firefox may need permission
✓ Try allowing camera: Settings → Privacy → Camera
```

### "Port 5000 already in use"
```bash
Open app.py, find line: app.run(port=5000)
Change to: app.run(port=5001)
Restart the server
```

### "AttributeError in app.py"
```bash
Delete attendance.db file
Restart app.py (database will be recreated)
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
pip install --upgrade pip
```

### "Face not detected"
```bash
✓ Ensure clear lighting
✓ Use same photo format as original upload
✓ Reinstall with better quality photo
✓ Check camera resolution is at least 640x480
```

## Check if Everything Installed Correctly

Run this command:
```bash
python -c "import flask, cv2, face_recognition; print('✓ All packages installed')"
```

Expected: `✓ All packages installed`

## File Check

Before starting, verify these files exist:
```
✓ app.py
✓ requirements.txt
✓ templates/base.html
✓ templates/dashboard.html
✓ templates/admin.html
✓ templates/attendance.html
✓ templates/reports.html
```

If missing, the web files may not have been created properly.

## Database Initialization

The first time you run `python app.py`:
1. System automatically creates `attendance.db`
2. Database tables are created (Student, Attendance)
3. `uploads/` folder is created for photos
4. You're ready to add students!

## Recommended First Test

1. Add 3-4 test students
2. Upload clear photos
3. Test face recognition
4. Check attendance marks
5. View reports
6. If all working → Ready for production!

## Stop the Server

To stop the application:
```bash
Press CTRL+C in the terminal
```

Output:
```
Keyboard interrupt received, exiting.
```

## Restart the Server

After making changes or restarting system:
```bash
python app.py
```

Server will start on same port and load existing data.

## Next Steps

- ✅ Complete first time setup above
- ✅ Add 5-10 real students
- ✅ Test face recognition with different lighting
- ✅ Verify attendance is logged correctly
- ✅ Check reports are accurate
- ✅ Share access details with teachers/admins

## Performance Tips

- Use modern browser (Chrome, Firefox, Edge)
- Good internet connection (even for local network)
- Clear browser cache if slow
- Close background applications
- Ensure webcam is good quality

## Getting Help

| Issue | Solution |
|-------|----------|
| App won't start | Check Python path, reinstall requirements |
| No webcam | Grant browser permissions, check hardware |
| Face not recognized | Better lighting, clearer photo |
| Slow performance | Close other apps, clear cache |
| Database error | Delete attendance.db, restart |

## Success Checklist

- [ ] pip install -r requirements.txt successful
- [ ] python app.py runs without errors
- [ ] Browser loads http://localhost:5000
- [ ] Can add a student with photo
- [ ] Can start webcam camera
- [ ] Face is detected properly
- [ ] Can mark attendance
- [ ] Attendance shows in reports

**Once all checked ✓ → You're ready to roll! 🎉**

## For Teachers/Staff

Share this access:
```
Open browser → http://localhost:5000
Go to Mark Attendance → Start Camera → Record attendance
No additional setup needed!
```

## Advanced (Optional)

Customize in `app.py`:
- Line 35: Change face matching threshold (0.6 default)
- Line 48: Change upload folder location
- Last line: Change port/host

---

**That's it! Your system is now running.** 🚀

For detailed information, see README_WEB.md
