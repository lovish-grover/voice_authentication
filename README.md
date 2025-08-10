# 🎤 Voice Authentication System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

> A **real-time voice authentication system** using **MFCC features** + **Machine Learning** to securely verify users based on their unique voice characteristics.

---

## 📌 Features

✅ **Voice Registration** – Record and store unique voice samples  
✅ **Real-Time Verification** – Authenticate instantly via browser microphone  
✅ **MFCC Feature Extraction** – Captures unique vocal signatures  
✅ **Data Augmentation** – Improves model robustness  
✅ **Persistent Model** – Saved model (`trained_model.json`) for fast re-use  
✅ **Clean Web Interface** – HTML + JS frontend for seamless experience  

---

## 🛠️ Tech Stack

### **Backend**
- Python 3.10+
- Flask – Web framework
- Librosa – Audio processing & MFCC extraction
- Scikit-learn – Model training & classification
- NumPy, Pandas – Data handling

### **Frontend**
- HTML, CSS
- JavaScript (Web Audio API for mic recording)

---

## 📂 Project Structure

voice_authentication/
│
├── audio_processing.py # Audio loading, segmentation, augmentation
├── authentication.py # Verification logic
├── database.py # User database handling
├── feature_extraction.py # MFCC feature extraction
├── model_training.py # Model training
├── main.py # Flask app entry point
├── trained_model.json # Saved ML model
│
├── static/
│ ├── recorder.js # Mic recording logic
│ └── style.css # Styling
│
├── templates/
│ ├── train.html # Registration page
│ └── verify.html # Verification page
│
├── uploads/ # Stored voice samples
└── README.md
