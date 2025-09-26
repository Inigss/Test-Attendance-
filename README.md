# 🎯 Face Recognition Attendance System

A modern, OpenCV-based face recognition attendance system built with Python. This project provides real-time face detection and recognition capabilities for automated attendance tracking.

## ✨ Features

- 🔍 **Real-time Face Detection** - Detect faces from webcam feed
- 👤 **Face Recognition** - Recognize registered students automatically  
- 📊 **Attendance Tracking** - Automatic attendance marking with timestamps
- 🗄️ **Database Integration** - SQLite and MySQL support
- 📈 **Reporting** - Generate attendance reports and analytics
- 🖥️ **GUI Ready** - Compatible with Tkinter and PyQt5 interfaces
- 📱 **Cross-platform** - Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested with Python 3.13.7)
- Webcam/Camera access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Inigss/Test-Attendance-.git
   cd Test-Attendance-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux  
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the demo**
   ```bash
   python face_recognition_opencv.py
   ```

## 🎬 Demo

The demo will:
- Open your camera
- Detect faces in real-time
- Draw bounding boxes around detected faces
- Press 'q' to quit

## 🛠️ Technology Stack

- **OpenCV (opencv-contrib-python)** - Computer vision and face recognition
- **NumPy** - Numerical computations and array operations
- **Pandas** - Data manipulation and analysis
- **SQLite/MySQL** - Database storage
- **Tkinter/PyQt5** - GUI frameworks
- **Matplotlib** - Data visualization

## 📁 Project Structure

```
Test-Attendance-/
├── face_recognition_opencv.py  # Main face recognition system
├── requirements.txt           # Python dependencies
├── SETUP_GUIDE.md            # Detailed setup instructions
├── SUCCESS_REPORT.md         # Installation success report
├── .gitignore               # Git ignore rules
└── README.md               # This file
```

## 🔧 Configuration

### Face Recognition Settings
- **Detection Model**: Haar Cascade Classifier
- **Recognition Algorithm**: LBPH (Local Binary Patterns Histograms)
- **Confidence Threshold**: 50 (adjustable)

### Database Schema
- **Students Table**: ID, Name, Student ID, Registration Date
- **Attendance Table**: ID, Student ID, Name, Timestamp

## 📖 Usage Examples

### Basic Face Detection
```python
import cv2

# Initialize the system
system = FaceRecognitionAttendance()

# Detect faces in an image
faces = system.detect_faces(image)
```

### Student Registration
```python
# Register a new student
success = system.add_student(
    name="John Doe",
    student_id="STU001", 
    face_images=[img1, img2, img3]
)
```

### Mark Attendance
```python
# Recognize and mark attendance
recognized = system.recognize_face(camera_image)
if recognized:
    system.mark_attendance(recognized[0]['student_id'])
```

## 🎯 Roadmap

- [ ] Web interface using Flask/FastAPI
- [ ] Mobile app integration
- [ ] Advanced recognition algorithms
- [ ] Cloud database support
- [ ] Batch processing for images
- [ ] Export to Excel/PDF reports

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🛟 Support

If you encounter any issues:

1. Check the `SETUP_GUIDE.md` for detailed setup instructions
2. Review the `SUCCESS_REPORT.md` for troubleshooting tips
3. Create an issue on GitHub with detailed error information

## 🙏 Acknowledgments

- OpenCV community for excellent computer vision libraries
- Python community for robust ecosystem
- Contributors who help improve this project

---

⭐ **Star this repository if it helped you!** ⭐