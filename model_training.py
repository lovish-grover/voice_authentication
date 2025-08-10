# model_training.py
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_xgboost(features, labels, model_path="trained_model.json"):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    
    xgb_model = xgb.XGBClassifier(
        objective='multi:softprob',  # Multi-class with probabilities
        eval_metric='mlogloss',      # Multi-class log loss
        num_class=len(np.unique(labels))  # Number of unique users
    )
    xgb_model.fit(X_train, y_train)
    
    # Predict class labels explicitly
    y_pred_proba = xgb_model.predict_proba(X_test)  # Get probability matrix
    y_pred = np.argmax(y_pred_proba, axis=1)       # Convert to class labels
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {accuracy}")
    
    # Save the model
    xgb_model.save_model(model_path)
    return xgb_model