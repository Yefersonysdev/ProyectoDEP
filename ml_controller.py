from fastapi import APIRouter, HTTPException, status, Path
from model import Values
import pickle
from typing import List

#Librerias para modelo de Regresión Logistica
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler


router = APIRouter()
preds = []
current_id = 0

# Cargar el modelo al inicio del controlador
ML_MODEL = 'modelo.pkl'

with open(ML_MODEL, 'rb') as file:
    loaded_model = pickle.load(file)

def predict(data: Values, model):
    global current_id
    # Extraer los valores de Accuracy, conf_matrix y roc_auc
    accuracy = data.Accuracy
    conf_matrix = np.array(data.conf_matrix)
    roc_auc = data.roc_auc

    # Crear un array 2D con estos valores
    input_data = np.array([[accuracy, *conf_matrix.flatten(), roc_auc] * 5])  # Repetir 5 veces para obtener 30 características

    # Realizar la predicción y obtener la probabilidad
    prediction = model.predict(input_data)
    proba = model.predict_proba(input_data)[:, 1]

    result = {
        "id": current_id + 1,
        "prediction": int(prediction),
        "probability": float(proba),
    }
    current_id += 1
    return result




@router.get('/ml')
def get_task():
    return preds

@router.post('/ml', status_code=status.HTTP_201_CREATED)
def endpoint_predic(data: Values):

    result = predict(data, loaded_model)
    # Agrega el resultado a la lista
    preds.append(result)
    return result , {"message": "Modelo agregado correctamente"}



@router.delete('/ml/{pred_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_pred(pred_id: int = Path(..., title="The ID of the prediction to delete")):
    for pred_item in preds:
        if pred_item["id"] == pred_id:
            preds.remove(pred_item)
            return {"Borrado correctamente"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID no encontrado')
