import pickle
import os
import numpy as np

from apps.core.cache import get_cached_prediction, set_cached_prediction

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, 'models/fraud_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'models/scaler.pkl')
ISO_PATH = os.path.join(BASE_DIR, 'models/iso_forest.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'models/label_encoders.pkl')


model = None
scaler = None
iso_forest = None
encoders = None


def load_artifacts():
    global model, scaler, iso_forest, encoders

    if model is None:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

    if scaler is None:
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

    if iso_forest is None:
        with open(ISO_PATH, 'rb') as f:
            iso_forest = pickle.load(f)

    if encoders is None:
        with open(ENCODER_PATH, 'rb') as f:
            encoders = pickle.load(f)


def predict(features: dict) -> float:
    try:
        # Check for cached data
        cached = get_cached_prediction(features)
        if cached is not None:
            print("Cache HIT")
            return cached
        
        print("Cache MISS")
        load_artifacts()

        amount = float(features["amount"])
        location = features["location"]
        device = features["device"]

        # Encode
        location_encoded = encoders["location"].transform([location])[0]
        device_encoded = encoders["device"].transform([device])[0]

        # Base features
        X = np.array([[amount, location_encoded, device_encoded]])

        # Scale
        X_scaled = scaler.transform(X)

        # Anomaly score
        anomaly = iso_forest.predict(X_scaled)[0]
        anomaly = 1 if anomaly == -1 else 0

        # Final feature vector (VERY IMPORTANT)
        final_features = np.array([[
            X_scaled[0][0],   # scaled amount
            X_scaled[0][1],   # scaled location
            X_scaled[0][2],   # scaled device
            anomaly
        ]])

        # Prediction
        probability = model.predict_proba(final_features)[0][1]

        # Set cached data
        set_cached_prediction(features, probability)

        return float(probability)

    except Exception as e:
        print(f"Error in prediction: {e}")
        return 0.0