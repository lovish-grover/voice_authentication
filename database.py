# database.py
import mysql.connector
import numpy as np

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="voice_user",
        password="password123",
        database="voice_auth"
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL
        )
    """)
    
    # Create audio_files table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audio_files (
            file_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            file_path VARCHAR(255) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Create features table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS features (
            feature_id INT AUTO_INCREMENT PRIMARY KEY,
            file_id INT,
            feature_vector BLOB NOT NULL,
            FOREIGN KEY (file_id) REFERENCES audio_files(file_id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def add_user(user_name, audio_files, features):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert user
    cursor.execute("INSERT INTO users (user_name) VALUES (%s)", (user_name,))
    user_id = cursor.lastrowid
    
    # Insert audio files and features
    for file_path, feature_vector in zip(audio_files, features):
        cursor.execute("INSERT INTO audio_files (user_id, file_path) VALUES (%s, %s)", (user_id, file_path))
        file_id = cursor.lastrowid
        feature_blob = feature_vector.tobytes()
        cursor.execute("INSERT INTO features (file_id, feature_vector) VALUES (%s, %s)", (file_id, feature_blob))
    
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

def get_training_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user data
    cursor.execute("SELECT user_id, user_name FROM users")
    user_rows = cursor.fetchall()
    original_user_ids = [row[0] for row in user_rows]
    user_names = [row[1] for row in user_rows]
    
    # Remap user_ids to start from 0
    id_map = {original_id: new_id for new_id, original_id in enumerate(original_user_ids)}
    user_map = {new_id: name for new_id, name in enumerate(user_names)}
    
    # Get features and labels
    cursor.execute("""
        SELECT f.feature_vector, a.user_id
        FROM features f
        JOIN audio_files a ON f.file_id = a.file_id
    """)
    features = []
    labels = []
    for feature_blob, user_id in cursor.fetchall():
        feature_vector = np.frombuffer(feature_blob, dtype=np.float64)
        features.append(feature_vector)
        labels.append(id_map[user_id])  # Remap to new label
    
    cursor.close()
    conn.close()
    return np.array(features), np.array(labels), user_map

if __name__ == "__main__":
    init_db()