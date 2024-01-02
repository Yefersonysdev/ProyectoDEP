import pickle
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler

def train_and_save_model(X, y, test_size=0.2, random_state=42):
    # Feature Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Dividir los datos
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=test_size, random_state=random_state)

    # Entrenar el modelo
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)

    # Test del modelo
    y_pred = logreg.predict(X_test)
    y_pred_proba = logreg.predict_proba(X_test)[:, 1]

    # Cross-validation
    scores = cross_val_score(logreg, X_scaled, y, cv=5, scoring='accuracy')
    # print(f'Cross-Validation Accuracy Scores: {scores}')
    # print(f'Average Cross-Validation Accuracy Score: {np.mean(scores)}')

    # Guardar el modelo en un archivo
    with open('modelo.pkl', 'wb') as file:
        pickle.dump(logreg, file)

    return logreg

# Cargar datos
data = load_breast_cancer()
X, y = data.data, data.target

# Entrenar y guardar el modelo
trained_model = train_and_save_model(X, y)

# Cargar el modelo desde el archivo
with open('modelo.pkl', 'rb') as file:
    loaded_model = pickle.load(file)
