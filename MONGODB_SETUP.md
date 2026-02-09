# 🌐 MongoDB Atlas Setup Guide

## Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a **FREE** account
3. Verify your email

## Step 2: Create a Cluster

1. Click **"Build a Database"**
2. Choose **"M0 FREE"** tier
3. Select your preferred cloud provider and region (choose closest to you)
4. Click **"Create Cluster"**
5. Wait 3-5 minutes for cluster creation

## Step 3: Create Database User

1. Click **"Database Access"** in left sidebar
2. Click **"Add New Database User"**
3. Set authentication method: **"Password"**
4. Username: `attendanceUser` (or your choice)
5. Password: Generate a strong password (save it!)
6. Database User Privileges: **"Read and write to any database"**
7. Click **"Add User"**

## Step 4: Configure Network Access

1. Click **"Network Access"** in left sidebar
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - For production, restrict to your IP only
4. Click **"Confirm"**

## Step 5: Get Connection String

1. Go back to **"Database"** (Deployment → Database)
2. Click **"Connect"** button on your cluster
3. Choose **"Connect your application"**
4. Driver: **Python**, Version: **3.12 or later**
5. Copy the connection string (looks like):
   ```
   mongodb+srv://attendanceUser:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 6: Configure Your Application

### Create `.env` file:

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file and update:
   ```env
   MONGODB_URI=mongodb+srv://attendanceUser:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/attendance_db?retryWrites=true&w=majority
   SECRET_KEY=your-secret-key-here
   UPLOAD_FOLDER=uploads
   MAX_CONTENT_LENGTH=16777216
   ```

3. Replace:
   - `YOUR_PASSWORD` with your database user password
   - `cluster0.xxxxx.mongodb.net` with your cluster hostname
   - `your-secret-key-here` with a random secret key

### Generate Secret Key:
```python
import secrets
print(secrets.token_hex(32))
```

## Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

New packages installed:
- `pymongo`: MongoDB driver for Python
- `dnspython`: Required for MongoDB Atlas connection

## Step 8: Switch to MongoDB Version

### Option 1: Rename files (Recommended)
```bash
# Backup old SQLite version
move app.py app_sqlite.py

# Use MongoDB version
move app_mongodb.py app.py
```

### Option 2: Just use MongoDB file directly
```bash
python app_mongodb.py
```

## Step 9: Run Application

```bash
python app.py
```

You should see:
```
✅ Connected to MongoDB successfully!
🚀 Starting Flask app...
📁 Upload folder: uploads
🗄️  Database: MongoDB
🌐 Server: http://localhost:5000
```

## ✅ Verification Checklist

- [ ] MongoDB Atlas account created
- [ ] Cluster created and running (green status)
- [ ] Database user created with password
- [ ] Network access configured (0.0.0.0/0)
- [ ] Connection string copied
- [ ] `.env` file created with MONGODB_URI
- [ ] Dependencies installed (`pymongo`, `dnspython`)
- [ ] Application runs without errors
- [ ] Can add students via Admin Panel
- [ ] Can mark attendance
- [ ] Data persists in MongoDB Atlas

## 🔍 View Your Data in Atlas

1. Go to MongoDB Atlas Dashboard
2. Click **"Browse Collections"** on your cluster
3. Database: `attendance_db`
4. Collections:
   - `students` - Student information
   - `attendance` - Attendance records

## 📊 Data Structure

### Students Collection:
```json
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "roll_number": "001",
  "photo_path": "uploads/001_photo.jpg",
  "face_encoding": Binary("..."),
  "created_at": ISODate("2026-02-09T...")
}
```

### Attendance Collection:
```json
{
  "_id": ObjectId("..."),
  "student_id": ObjectId("..."),
  "date": "2026-02-09",
  "time": "12:30:45"
}
```

## 🔒 Security Best Practices

1. **Never commit `.env` file** to Git:
   ```bash
   echo .env >> .gitignore
   ```

2. **Use strong passwords** for database users

3. **Restrict IP access** in production:
   - Remove 0.0.0.0/0
   - Add only your server's IP address

4. **Rotate secret keys** periodically

5. **Enable MongoDB Atlas monitoring** and alerts

## 🚨 Troubleshooting

### "Failed to connect to MongoDB"
- Check internet connection
- Verify MONGODB_URI in `.env` file
- Ensure password doesn't contain special characters (or URL-encode them)
- Check network access allows your IP (0.0.0.0/0 for testing)

### "Authentication failed"
- Verify username and password in connection string
- Check database user exists in Database Access
- Ensure user has proper permissions

### "Module not found: pymongo"
```bash
pip install pymongo dnspython
```

### "ServerSelectionTimeoutError"
- Check internet connection
- Verify cluster is running (green status in Atlas)
- Check firewall isn't blocking MongoDB ports

## 🔄 Migration from SQLite

If you have existing data in SQLite (`attendance.db`), you can migrate:

1. Install additional tool:
   ```bash
   pip install sqlite3
   ```

2. Create migration script:
   ```python
   # migrate_to_mongo.py
   import sqlite3
   from pymongo import MongoClient
   from datetime import datetime
   
   # Connect to SQLite
   sqlite_conn = sqlite3.connect('attendance.db')
   cursor = sqlite_conn.cursor()
   
   # Connect to MongoDB
   mongo_client = MongoClient('your_mongodb_uri')
   db = mongo_client.attendance_db
   
   # Migrate students
   cursor.execute("SELECT * FROM student")
   for row in cursor.fetchall():
       student = {
           'name': row[1],
           'roll_number': row[2],
           'photo_path': row[3],
           'face_encoding': row[4],
           'created_at': datetime.fromisoformat(row[5])
       }
       db.students.insert_one(student)
   
   print("✅ Migration complete!")
   ```

## 🆘 Support

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB University](https://university.mongodb.com/) - Free courses

## 🎉 Benefits of MongoDB Atlas

✅ **Cloud-hosted** - No local database management
✅ **Free tier** - 512MB storage forever free
✅ **Automatic backups** - Point-in-time recovery
✅ **Scalable** - Easy upgrade as you grow
✅ **Secure** - Built-in encryption and authentication
✅ **Global** - Deploy across multiple regions
✅ **Monitoring** - Real-time performance metrics
✅ **Access from anywhere** - No local setup needed

Your data is now stored in the cloud! 🌐
