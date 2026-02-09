from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import os
import face_recognition
import numpy as np
import cv2
import base64
from datetime import datetime, date
from io import BytesIO
from PIL import Image
import json
from pymongo import MongoClient
from bson import ObjectId, Binary
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'attendance-system-secret')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file

# MongoDB Atlas Connection
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("⚠️ MONGODB_URI not found in .env file!")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    raise

db = client.attendance_db
students_collection = db.students
attendance_collection = db.attendance

# Helper Functions
def student_to_dict(student):
    """Convert MongoDB student document to dictionary"""
    return {
        'id': str(student['_id']),
        'name': student['name'],
        'roll_number': student['roll_number'],
        'created_at': student.get('created_at', datetime.now()).isoformat() if isinstance(student.get('created_at'), datetime) else str(student.get('created_at', ''))
    }

def attendance_to_dict(attendance):
    """Convert MongoDB attendance document to dictionary"""
    student = students_collection.find_one({'_id': attendance['student_id']})
    att_datetime = attendance['datetime']
    # Extract date and time from datetime object
    if isinstance(att_datetime, datetime):
        date_str = att_datetime.strftime('%Y-%m-%d')
        time_str = att_datetime.strftime('%H:%M:%S')
    else:
        date_str = str(att_datetime)
        time_str = '00:00:00'
    
    return {
        'id': str(attendance['_id']),
        'student_name': student['name'] if student else 'Unknown',
        'student_roll': student['roll_number'] if student else 'N/A',
        'date': date_str,
        'time': time_str
    }

# Route to serve photos from MongoDB
@app.route('/photo/<student_id>')
def get_photo(student_id):
    """Serve student photo from MongoDB"""
    try:
        student = students_collection.find_one({'_id': ObjectId(student_id)})
        if student and 'photo_data' in student:
            return send_file(
                BytesIO(student['photo_data']),
                mimetype='image/jpeg',
                as_attachment=False
            )
        return jsonify({'error': 'Photo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes
@app.route('/')
def dashboard():
    """Main dashboard"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    total_students = students_collection.count_documents({})
    present_today = attendance_collection.count_documents({
        'datetime': {'$gte': today_start, '$lte': today_end}
    })
    
    if total_students > 0:
        attendance_percentage = (present_today / total_students) * 100
    else:
        attendance_percentage = 0
    
    return render_template('dashboard.html', 
                         total_students=total_students,
                         present_today=present_today,
                         attendance_percentage=round(attendance_percentage, 1))

@app.route('/admin')
def admin():
    """Admin panel - manage students"""
    students = list(students_collection.find())
    students = [student_to_dict(s) for s in students]
    return render_template('admin.html', students=students)

@app.route('/attendance')
def attendance_page():
    """Attendance marking page"""
    return render_template('attendance.html')

@app.route('/reports')
def reports():
    """View attendance reports"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    today_attendance = list(attendance_collection.find({
        'datetime': {'$gte': today_start, '$lte': today_end}
    }))
    today_attendance = [attendance_to_dict(a) for a in today_attendance]
    
    total_students = students_collection.count_documents({})
    
    # Get all students with their stats
    students = list(students_collection.find())
    students_data = []
    for student in students:
        total_attendance = attendance_collection.count_documents({'student_id': student['_id']})
        students_data.append({
            'id': str(student['_id']),
            'name': student['name'],
            'roll_number': student['roll_number'],
            'total_attendance': total_attendance
        })
    
    return render_template('reports.html', 
                        attendance=today_attendance,
                         total_students=total_students,
                         students_data=students_data)

# API Routes
@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    students = list(students_collection.find())
    return jsonify([student_to_dict(s) for s in students])

@app.route('/api/students/add', methods=['POST'])
def add_student():
    """Add new student - stores photo in MongoDB cloud"""
    try:
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        photo = request.files.get('photo')
        
        if not all([name, roll_number, photo]):
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        
        # Check if student exists
        if students_collection.find_one({'roll_number': roll_number}):
            return jsonify({'success': False, 'message': 'Roll number already exists'}), 400
        
        # Read photo into memory (don't save to disk)
        photo_bytes = photo.read()
        
        # Process image for face detection
        try:
            image = Image.open(BytesIO(photo_bytes))
            image_np = np.array(image)
            
            # Detect face locations
            face_locations = face_recognition.face_locations(image_np, model='hog')
            
            if len(face_locations) == 0:
                return jsonify({'success': False, 'message': 'No face detected in image. Please ensure the face is clearly visible.'}), 400
            
            # If multiple faces detected, use the largest one (most prominent)
            if len(face_locations) > 1:
                def face_area(location):
                    top, right, bottom, left = location
                    return (bottom - top) * (right - left)
                
                largest_face = max(face_locations, key=face_area)
                face_locations = [largest_face]
                print(f"Multiple faces detected, using the largest/most prominent face")
            
            # Get encoding for the selected face
            face_encodings = face_recognition.face_encodings(image_np, face_locations)
            
            if len(face_encodings) == 0:
                return jsonify({'success': False, 'message': 'Could not encode face. Please use a clearer image.'}), 400
            
            face_encoding = face_encodings[0]
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error processing image: {str(e)}'}), 400
        
        # Save student to MongoDB (photo stored as binary in cloud)
        student_doc = {
            'name': name,
            'roll_number': roll_number,
            'photo_data': Binary(photo_bytes),  # Store photo in MongoDB
            'face_encoding': Binary(face_encoding.tobytes()),
            'created_at': datetime.now()
        }
        result = students_collection.insert_one(student_doc)
        
        print(f"✅ Student added to MongoDB cloud: {name} (ID: {result.inserted_id})")
        return jsonify({'success': True, 'message': 'Student added successfully'}), 201
    
    except Exception as e:
        print(f"❌ Error adding student: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete student from MongoDB"""
    try:
        result = students_collection.delete_one({'_id': ObjectId(student_id)})
        
        if result.deleted_count == 0:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        # Also delete attendance records
        attendance_collection.delete_many({'student_id': ObjectId(student_id)})
        
        print(f"✅ Student deleted from MongoDB cloud: {student_id}")
        return jsonify({'success': True, 'message': 'Student deleted'})
    
    except Exception as e:
        print(f"❌ Error deleting student: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/students/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update student information in MongoDB"""
    try:
        student = students_collection.find_one({'_id': ObjectId(student_id)})
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        photo = request.files.get('photo')
        
        update_data = {}
        
        # Update name if provided
        if name:
            update_data['name'] = name
        
        # Update roll number if provided and not duplicate
        if roll_number and roll_number != student['roll_number']:
            existing = students_collection.find_one({'roll_number': roll_number})
            if existing:
                return jsonify({'success': False, 'message': 'Roll number already exists'}), 400
            update_data['roll_number'] = roll_number
        
        # Update photo if provided
        if photo:
            # Read new photo into memory
            photo_bytes = photo.read()
            
            # Process image for face detection
            try:
                image = Image.open(BytesIO(photo_bytes))
                image_np = np.array(image)
                
                face_locations = face_recognition.face_locations(image_np, model='hog')
                
                if len(face_locations) == 0:
                    return jsonify({'success': False, 'message': 'No face detected in image'}), 400
                
                if len(face_locations) > 1:
                    def face_area(location):
                        top, right, bottom, left = location
                        return (bottom - top) * (right - left)
                    largest_face = max(face_locations, key=face_area)
                    face_locations = [largest_face]
                
                face_encodings = face_recognition.face_encodings(image_np, face_locations)
                if len(face_encodings) == 0:
                    return jsonify({'success': False, 'message': 'Could not encode face'}), 400
                
                # Store photo and encoding in MongoDB
                update_data['photo_data'] = Binary(photo_bytes)
                update_data['face_encoding'] = Binary(face_encodings[0].tobytes())
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error processing image: {str(e)}'}), 400
        
        # Update in MongoDB
        if update_data:
            students_collection.update_one(
                {'_id': ObjectId(student_id)},
                {'$set': update_data}
            )
        
        print(f"✅ Student updated in MongoDB cloud: {student_id}")
        return jsonify({'success': True, 'message': 'Student updated successfully'})
    
    except Exception as e:
        print(f"❌ Error updating student: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/students/<string:student_id>/stats', methods=['GET'])
def get_student_stats(student_id):
    """Get individual student statistics from MongoDB"""
    try:
        student = students_collection.find_one({'_id': ObjectId(student_id)})
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        # Get all attendance records
        attendance_records = list(attendance_collection.find(
            {'student_id': ObjectId(student_id)}
        ).sort([('datetime', -1)]))
        
        # Calculate stats
        created_at = student.get('created_at', datetime.now())
        if isinstance(created_at, datetime):
            total_days = (datetime.now().date() - created_at.date()).days + 1
        else:
            total_days = 1
            
        total_attended = len(attendance_records)
        attendance_percentage = (total_attended / total_days * 100) if total_days > 0 else 0
        
        # Format attendance records
        records = []
        for record in attendance_records:
            rec_datetime = record['datetime']
            # Extract date and time from datetime object
            if isinstance(rec_datetime, datetime):
                date_str = rec_datetime.strftime('%Y-%m-%d')
                time_str = rec_datetime.strftime('%H:%M:%S')
                day_str = rec_datetime.strftime('%A')
            else:
                # Fallback if not datetime
                date_str = str(rec_datetime)
                time_str = '00:00:00'
                day_str = 'Unknown'
            
            records.append({
                'date': date_str,
                'time': time_str,
                'day': day_str
            })
        
        return jsonify({
            'success': True,
            'student': {
                'name': student['name'],
                'roll_number': student['roll_number'],
                'enrolled_since': created_at.strftime('%Y-%m-%d') if isinstance(created_at, datetime) else str(created_at)
            },
            'stats': {
                'total_days': total_days,
                'total_attended': total_attended,
                'attendance_percentage': round(attendance_percentage, 1),
                'absent_days': total_days - total_attended
            },
            'records': records
        })
    except Exception as e:
        print(f"❌ Error getting student stats: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """Mark attendance from face recognition - all data in MongoDB"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image provided'}), 400
        
        # Decode image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Detect faces
        face_locations = face_recognition.face_locations(image_np)
        face_encodings = face_recognition.face_encodings(image_np, face_locations)
        
        if len(face_encodings) == 0:
            return jsonify({'success': False, 'message': 'No faces detected'}), 400
        
        marked_students = []
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        now = datetime.now()
        
        # Get all students with encodings from MongoDB
        students = list(students_collection.find({'face_encoding': {'$exists': True}}))
        known_encodings = []
        student_map = {}
        
        for idx, student in enumerate(students):
            if 'face_encoding' in student:
                encoding = np.frombuffer(student['face_encoding'], dtype=np.float64)
                known_encodings.append(encoding)
                student_map[idx] = student
        
        # Match faces
        for face_encoding in face_encodings:
            if len(known_encodings) == 0:
                continue
            
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(distances)
            best_distance = distances[best_match_index]
            
            if best_distance < 0.6:  # Recognition threshold
                student = student_map[best_match_index]
                
                # Check if already marked today
                existing = attendance_collection.find_one({
                    'student_id': student['_id'],
                    'datetime': {'$gte': today_start, '$lte': today_end}
                })
                
                if not existing:
                    # Mark attendance in MongoDB
                    attendance_collection.insert_one({
                        'student_id': student['_id'],
                        'datetime': now
                    })
                    marked_students.append({
                        'name': student['name'],
                        'roll': student['roll_number'],
                        'confidence': round((1 - best_distance) * 100, 1)
                    })
        
        if marked_students:
            print(f"✅ Marked attendance in MongoDB cloud for {len(marked_students)} student(s)")
            return jsonify({
                'success': True,
                'message': f'Marked {len(marked_students)} student(s)',
                'students': marked_students
            })
        else:
            return jsonify({'success': False, 'message': 'No students matched'}), 400
    
    except Exception as e:
        print(f"❌ Error marking attendance: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/attendance/today', methods=['GET'])
def get_todays_attendance():
    """Get today's attendance from MongoDB"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    attendance = list(attendance_collection.find({
        'datetime': {'$gte': today_start, '$lte': today_end}
    }))
    
    return jsonify([attendance_to_dict(a) for a in attendance])

@app.route('/api/attendance/reset', methods=['POST'])
def reset_attendance():
    """Reset today's attendance (admin only)"""
    try:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        result = attendance_collection.delete_many({
            'datetime': {'$gte': today_start, '$lte': today_end}
        })
        print(f"✅ Reset attendance in MongoDB: deleted {result.deleted_count} records")
        return jsonify({'success': True, 'message': 'Attendance reset'})
    except Exception as e:
        print(f"❌ Error resetting attendance: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    print(f"📁 Upload folder: No local storage - all data in MongoDB Atlas cloud")
    print(f"🗄️  Database: MongoDB Atlas")
    print(f"🌐 Server: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
