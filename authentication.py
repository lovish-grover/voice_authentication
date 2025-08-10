# authentication.py
import xgboost as xgb
import numpy as np
from feature_extraction import extract_features

def authenticate_audio(file_path, user_map, threshold=0.7, model_path="trained_model.json"):
    # Load the trained model
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    # Extract features and predict
    try:
        new_features = extract_features(file_path).reshape(1, -1)
        probabilities = model.predict_proba(new_features)[0]
        predicted_class = np.argmax(probabilities)
        confidence = probabilities[predicted_class]
        
        print(f"Predicted class: {predicted_class}, Confidence: {confidence:.2f}")
        if confidence >= threshold:
            user_name = user_map.get(predicted_class, "Unknown")
            return f"Authenticated as {user_name} (Confidence: {confidence:.2f})"
        else:
            return "Not authenticated (Confidence below threshold)"
    except Exception as e:
        return f"Error processing audio: {str(e)}"