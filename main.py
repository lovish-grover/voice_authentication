# main.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import numpy as np
from audio_processing import split_and_augment
from feature_extraction import extract_features
from model_training import train_xgboost
from authentication import authenticate_audio
from database import init_db, add_user, get_training_data
from pydub import AudioSegment

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database
init_db()

@app.route("/", methods=["GET", "POST"])
def train():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        audio_file = request.files.get("audio_file")
        
        if not user_name or not audio_file or audio_file.filename == "":
            flash("Please provide a name and audio file (upload or record).")
            return redirect(request.url)
        
        # Save audio file
        user_id = len(get_training_data()[2])  # Temporary ID for file naming
        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], f"user_{user_id}.wav")
        audio_file.save(audio_path)
        
        # Convert to valid WAV format
        try:
            audio = AudioSegment.from_file(audio_path)
            audio.export(audio_path, format="wav")
        except Exception as e:
            flash(f"Error processing audio file: {str(e)}")
            return redirect(request.url)
        
        # Process audio
        audio_files = split_and_augment(audio_path, f"user_{user_id}")
        features = np.array([extract_features(file) for file in audio_files])
        
        # Store in database
        add_user(user_name, audio_files, features)
        
        flash(f"Audio for {user_name} uploaded successfully! Add more users or train the model.")
        return redirect(request.url)
    
    # Get current user count from database
    _, _, user_data = get_training_data()
    return render_template("train.html", user_count=len(user_data))

@app.route("/train_model", methods=["POST"])
def train_model():
    features, labels, user_data = get_training_data()
    
    if len(user_data) < 2:
        flash("Please upload audio for at least 2 users before training.")
        return redirect(url_for("train"))
    
    print(f"Training with {len(features)} samples across {len(user_data)} users")
    train_xgboost(features, labels)
    flash("Model trained successfully!")
    return redirect(url_for("verify"))

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        verify_file = request.files.get("audio_file")
        if not verify_file or verify_file.filename == "":
            flash("Please upload or record an audio file.")
            return redirect(request.url)
        
        # Save verification file
        verify_path = os.path.join(app.config["UPLOAD_FOLDER"], "verify_audio.wav")
        verify_file.save(verify_path)
        
        # Convert to valid WAV format
        try:
            audio = AudioSegment.from_file(verify_path)
            audio.export(verify_path, format="wav")
        except Exception as e:
            flash(f"Error processing verification audio: {str(e)}")
            return redirect(request.url)
        
        # Get user data and authenticate
        _, _, user_data = get_training_data()
        result = authenticate_audio(verify_path, user_data)
        flash(result)
        return redirect(request.url)
    
    return render_template("verify.html")

if __name__ == "__main__":
    app.run(debug=True)