import pandas as pd
import pickle 
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest

from imblearn.over_sampling import SMOTE
import lightgbm as lgb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(BASE_DIR, "dataset.csv")

df = pd.read_csv(file_path)

# Encoding categorical values
le_location = LabelEncoder()
le_device = LabelEncoder()

df["location"] = le_location.fit_transform(df["location"])
df["device"] = le_device.fit_transform(df["device"])

features = ["amount", "location", "device"]
X = df[features]
y = df["is_fraud"]

# Standard Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Anomaly Detection using Isolation Forest

iso_forest = IsolationForest(contamination=0.03,
                             random_state=42
                          )   

X_scaled = pd.DataFrame(X_scaled, columns=features)

X_scaled["anomaly_score"] = iso_forest.fit_predict(X_scaled)
X_scaled["anomaly_score"] = X_scaled["anomaly_score"].map({1: 0, -1: 1})

X_train, X_test, y_train, y_test = train_test_split(X_scaled,y,
                                                    test_size=0.2,
                                                    random_state=42,
                                                    stratify=y)

# SMOTE

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Taining the model
model = lgb.LGBMClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

model.fit(X_train_resampled, y_train_resampled)

# Saving the model

model_dir = os.path.join(os.path.dirname(__file__), "../models")

os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "fraud_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

with open(os.path.join(model_dir, "iso_forest.pkl"), "wb") as f:
    pickle.dump(iso_forest, f)

with open(os.path.join(model_dir, "label_encoders.pkl"), "wb") as f:
    pickle.dump({
        "location": le_location,
        "device": le_device
    }, f)

print("Model training and saving completed successfully.")
