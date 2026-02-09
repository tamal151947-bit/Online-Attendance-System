# 📸Face Recognition Based Online Attendance System

A web-based Face Recognition Attendance System that automatically marks student attendance using a camera and stored student images. It provides an Admin Panel, Live Camera Attendance, and Detailed Attendance Reports.

## 🚀 Features

✅ Add & manage students with photo upload

✅ Face recognition based attendance marking

✅ Students can be marked only once per day

✅ Dashboard with real-time statistics

✅ Attendance reports (Present / Absent / Percentage)

✅ Individual student attendance history

✅ Responsive and modern UI

✅ Daily report auto refresh

## 🖥️ Screenshots

✔ Dashboard
<img width="1915" height="1051" alt="Screenshot 2026-02-09 210758" src="https://github.com/user-attachments/assets/3605b31f-2ea4-44e2-ad96-40eaea3124af" />


✔ Admin Panel (Add Student)
<img width="1902" height="1048" alt="Screenshot 2026-02-09 210809" src="https://github.com/user-attachments/assets/ec9f053c-8001-46dc-b968-0454a62fa572" />


✔ Mark Attendance (Camera)
<img width="1889" height="1006" alt="Screenshot 2026-02-09 210822" src="https://github.com/user-attachments/assets/2dff2d00-518e-406f-8162-262a514161d3" />


✔ Attendance Reports
<img width="1918" height="1023" alt="Screenshot 2026-02-09 210834" src="https://github.com/user-attachments/assets/8d0e45da-50b3-43c5-a624-ee372f3ce483" />


✔ Individual Student Details
<img width="1778" height="978" alt="Screenshot 2026-02-09 210844" src="https://github.com/user-attachments/assets/ae9cc1fd-e4bd-40b7-b56c-bac20b247119" />





## 🛠️ Tech Stack

Frontend:

HTML

CSS

JavaScript

Bootstrap

Backend:

Python (Flask)

Database:

SQLite

Face Recognition:

OpenCV

face-recognition (dlib)

## 📂 Project Structure
Online-Attendance-System/
│
├── static/

│   ├── css/

│   ├── js/

│   └── images/

│

├── templates/

│   ├── dashboard.html

│   ├── admin.html

│   ├── attendance.html

│   └── reports.html

│

├── app.py

├── requirements.txt

└── README.md


## ⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/tamal151947-bit/Online-Attendance-System.git
cd Online-Attendance-System

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
python app.py

4️⃣ Open in browser
http://127.0.0.1:5000

## 🧑‍🏫 How It Works

Admin adds students with name, roll number, and photo

System stores face encodings

Camera starts for attendance

Face is matched with stored student images

Attendance is marked automatically

Reports are generated instantly

## 📊 Modules
### 🏠 Dashboard

Total students

Present today

Attendance percentage

## ⚙ Admin Panel

Add new student

Upload photo

Edit / delete student

## 📷 Mark Attendance

Live camera feed

Automatic face detection

Prevents duplicate attendance

## 📑 Reports

Present students list

Absent count

Individual student history

## 🔒 Rules Implemented

✔ Student can be marked only once per day

✔ Daily report resets automatically

✔ Face must be clearly visible

✔ Avoid multiple faces in one frame

## 📌 Future Enhancements

Login system (Admin / Teacher)

Cloud database support

Excel export of reports

Mobile app version

Multi-class support

## 👨‍💻 Author

Tamal Kar

