# Alternative Face Recognition Solution for Attendance System
# Using OpenCV's built-in face detection and recognition capabilities

import cv2
import numpy as np
import os
import pickle
from datetime import datetime
import sqlite3

class FaceRecognitionAttendance:
    def __init__(self):
        """Initialize the face recognition attendance system using OpenCV"""
        # Load face detection cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize face recognizer
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Database setup
        self.setup_database()
        
        # Storage for known faces
        self.known_faces = []
        self.known_names = []
        
    def setup_database(self):
        """Setup SQLite database for attendance records"""
        self.conn = sqlite3.connect('attendance.db')
        cursor = self.conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                student_id TEXT NOT NULL UNIQUE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        ''')
        
        self.conn.commit()
        
    def detect_faces(self, image):
        """Detect faces in an image using OpenCV"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces, gray
    
    def add_student(self, name, student_id, face_images):
        """Add a new student to the system with their face data"""
        # Add to database
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO students (name, student_id) VALUES (?, ?)", (name, student_id))
            self.conn.commit()
            
            # Process face images and train recognizer
            face_data = []
            for img in face_images:
                faces, gray = self.detect_faces(img)
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    face_data.append(face_roi)
            
            # Save face data
            self.known_faces.extend(face_data)
            self.known_names.extend([student_id] * len(face_data))
            
            # Train the recognizer
            if len(self.known_faces) > 0:
                self.face_recognizer.train(self.known_faces, np.array([hash(name) % 100 for name in self.known_names]))
            
            return True
        except sqlite3.IntegrityError:
            return False
    
    def recognize_face(self, image):
        """Recognize faces in the given image"""
        faces, gray = self.detect_faces(image)
        recognized_students = []
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            
            if len(self.known_faces) > 0:
                label, confidence = self.face_recognizer.predict(face_roi)
                
                # If confidence is below threshold, consider it a match
                if confidence < 50:  # Adjust threshold as needed
                    # Find corresponding student
                    if label < len(self.known_names):
                        student_id = self.known_names[label]
                        recognized_students.append({
                            'student_id': student_id,
                            'confidence': confidence,
                            'bbox': (x, y, w, h)
                        })
        
        return recognized_students
    
    def mark_attendance(self, student_id):
        """Mark attendance for a student"""
        cursor = self.conn.cursor()
        
        # Get student name
        cursor.execute("SELECT name FROM students WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        
        if result:
            name = result[0]
            # Check if already marked today
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT * FROM attendance 
                WHERE student_id = ? AND date(timestamp) = ?
            """, (student_id, today))
            
            if not cursor.fetchone():
                # Mark attendance
                cursor.execute("""
                    INSERT INTO attendance (student_id, name) VALUES (?, ?)
                """, (student_id, name))
                self.conn.commit()
                return True
        return False
    
    def get_attendance_report(self, date=None):
        """Get attendance report for a specific date"""
        cursor = self.conn.cursor()
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT name, student_id, timestamp 
            FROM attendance 
            WHERE date(timestamp) = ?
            ORDER BY timestamp
        """, (date,))
        
        return cursor.fetchall()

# Demo usage function
def demo_face_detection():
    """Demo function to test OpenCV face detection"""
    print("Testing OpenCV Face Detection...")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return
    
    print("✅ Camera opened successfully")
    print("✅ Face cascade loaded successfully")
    print("Press 'q' to quit the demo")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, 'Face Detected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        cv2.imshow('Face Detection Demo', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Face detection demo completed successfully!")

if __name__ == "__main__":
    # Test the face detection
    demo_face_detection()