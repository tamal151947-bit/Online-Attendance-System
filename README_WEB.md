# 🎓 Face Recognition Attendance System - Web Version

A modern, user-friendly web-based attendance management system using face recognition technology.

## Features

✨ **Complete Features:**
- **Smart Face Recognition**: Real-time face detection and matching via webcam
- **Student Management**: Add/remove students through web interface
- **Real-time Marking**: Automatically mark attendance for multiple students
- **Beautiful Dashboard**: Modern, responsive UI with statistics
- **Attendance Reports**: View daily attendance with detailed records
- **Duplicate Prevention**: Students can only be marked once per day
- **Responsive Design**: Works on desktop, tablet, and mobile browsers

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (embedded database)
- **Frontend**: HTML5, CSS3, JavaScript
- **Face Recognition**: face_recognition library (dlib-based)
- **Computer Vision**: OpenCV
- **Webcam Access**: WebRTC API

## System Requirements

- Python 3.7+
- Modern web browser with webcam
- 500MB+ disk space
- 2GB+ RAM

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

### Step 3: Access in Browser

Open your web browser and go to:
```
http://localhost:5000
```

## Project Structure

```
Attendence/
├── app.py                      # Flask application
├── utils.py                    # Helper functions
├── requirements.txt            # Python dependencies
├── attendance.db               # Database (auto-created)
├── uploads/                    # Student photos
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── dashboard.html         # Main dashboard
│   ├── admin.html             # Student management
│   ├── attendance.html        # Face recognition page
│   └── reports.html           # Attendance records
└── static/                     # CSS/JS files
```

## Usage Guide

### 1. Add Students (Admin Panel)

1. Click **"⚙️ Admin Panel"** from navigation
2. Fill in student details:
   - Name (e.g., "John Doe")
   - Roll Number (e.g., "001")
   - Student Photo
3. Click **"Add Student"**
4. Wait for face recognition validation
5. Student will be added to the system

**Photo Requirements:**
- ✓ Clear, well-lit image
- ✓ Single person per photo
- ✓ Face clearly visible
- ✓ JPG, PNG, or BMP format

### 2. Mark Attendance

1. Click **"📷 Mark Attendance"** from navigation
2. Click **"Start Camera"** button
3. Students should look at camera (2-3 seconds)
4. Click **"Mark Attendance"** to capture frame
5. System will automatically recognize and mark students
6. Marked students appear in the list
7. Click **"Stop Camera"** when done

**Tips for Best Results:**
- ✓ Good lighting in the room
- ✓ Keep faces 30-60cm from camera
- ✓ Face should be clear and front-facing
- ✓ Mark attendance in same lighting as registration photo

### 3. View Reports

1. Click **"📈 Reports"** from navigation
2. See today's attendance summary:
   - Total students
   - Present count
   - Absent count
   - Attendance percentage
3. View detailed list of marked students with times

### 4. Manage Students

- Delete students by clicking **"Delete"** button in Admin Panel
- Double-check student photos are uploading correctly
- Re-register if student appearance changes significantly

## Features Explained

### Dashboard
- Real-time statistics
- Total students count
- Present today count
- Attendance percentage
- Quick links to features

### Admin Panel
- Add new students with photos
- Delete existing students
- View all registered students
- Drag-and-drop photo upload
- Face validation before saving

### Attendance Marking
- Live camera feed
- Real-time face detection
- Manual or automatic marking
- Marked students list
- Reset today's attendance (admin)

### Reports
- Today's attendance details
- Marked students with timestamps
- Attendance rate calculation
- Print-friendly layout

## Database

The system uses SQLite database with two main tables:

1. **Student Table**
   - ID, Name, Roll Number
   - Photo Path, Face Encoding
   - Created Date

2. **Attendance Table**
   - Student Reference, Date, Time

All data is stored locally in `attendance.db`

## Security & Privacy

✅ **Local Processing**: All face recognition happens locally
✅ **No Cloud Sync**: Data stays on your server
✅ **No External APIs**: Complete privacy
✅ **Secure Storage**: Face encodings stored safely
✅ **Easy Backup**: Single database file to backup

## Troubleshooting

### Camera Not Working
1. Check browser permissions
2. Allow camera access when prompted
3. Try different browser
4. Verify webcam is connected

### Face Not Recognized
1. Ensure good lighting
2. Update student photo
3. Check face is clearly visible
4. Adjust confidence threshold in code if needed

### Database Errors
1. Delete `attendance.db` to reset
2. System will recreate on startup
3. All students data will be lost

### Port Already in Use
Change port in app.py:
```python
app.run(port=5001)  # Use different port
```

## Performance Optimization

- Limit to 500+ students for best performance
- Use good quality webcam (1080p+)
- Ensure adequate lighting
- Close unnecessary browser tabs
- Clear browser cache if slow

## Future Enhancements

- [ ] Export to Excel/CSV
- [ ] Email/SMS notifications
- [ ] Mobile app version
- [ ] Cloud backup option
- [ ] Multi-location support
- [ ] Advanced analytics
- [ ] Offline mode
- [ ] SSL/HTTPS security

## File Descriptions

### app.py
Main Flask application with:
- Routes for all pages
- API endpoints
- Database models
- Face recognition logic
- Image processing

### utils.py
Helper functions for:
- Face encoding/decoding
- Image processing
- Database operations

### templates/
HTML templates for:
- Navigation and layout
- Forms and input
- Display and reports
- Responsive design

## Running on Different Ports

Default: `localhost:5000`

To run on different port:
```bash
python app.py --port 8080
```

## Command Line Options

```bash
# Run on specific port
python app.py --port 5001

# Debug mode (auto-reload)
python app.py --debug

# Specific host
python app.py --host 192.168.1.100
```

## First Time Setup

1. Install requirements
2. Run app.py
3. Open browser to localhost:5000
4. Add 2-3 test students
5. Test face recognition
6. Adjust if needed
7. Ready for production use

## Backup & Restore

### Backup
Copy these files:
- `attendance.db` (database)
- `uploads/` folder (photos)

### Restore
Paste files back to original location and restart app

## Statistics & Reporting

The system tracks:
- Daily attendance records
- Student enrollment date
- Attendance percentage
- Peak marking times
- Recognition confidence scores

## Tips for Success

1. **Good Lighting**: Best results with natural light
2. **Clear Photos**: One face per student photo
3. **Regular Updates**: Update photos yearly
4. **Backup Data**: Weekly database backups
5. **Train Staff**: Show teachers how to use
6. **Test First**: Test with small group first

## Support

For issues or questions:
1. Check Troubleshooting section
2. Verify all dependencies installed
3. Check browser console for errors
4. Ensure webcam permissions granted

## License

This project is for educational and institutional use.

## Version

**Web Version**: 1.0.0
**Release Date**: February 9, 2026

---

**Ready to use! Access your system at http://localhost:5000** 🚀

For detailed usage instructions, use the Help menu in the application.
