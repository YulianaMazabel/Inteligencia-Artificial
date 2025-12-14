import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Dataset simulado del SITP / TransMilenio
data = {
    "distancia_km": [12, 15, 8, 20, 10, 9, 18, 7],
    "tiempo_min": [45, 70, 30, 90, 40, 35, 80, 25],
    "num_transbordos": [1, 3, 0, 4, 2, 1, 3, 0],
    "hora_pico": [1, 1, 0, 1, 0, 0, 1, 0],
    "ruta_optima": [1, 0, 1, 0, 1, 1, 0, 1]
}

df = pd.DataFrame(data)

# Variables de entrada y salida
X = df.drop("ruta_optima", axis=1)
y = df["ruta_optima"]

# División entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Entrenamiento del Árbol de Decisión
modelo = DecisionTreeClassifier(criterion="entropy", max_depth=3)
modelo.fit(X_train, y_train)

# Evaluación
y_pred = modelo.predict(X_test)
print("Resultados del modelo:\n")
print(classification_report(y_test, y_pred))

# Prueba manual
nueva_ruta = [[9, 35, 1, 0]]  # distancia, tiempo, transbordos, hora pico
prediccion = modelo.predict(nueva_ruta)

if prediccion[0] == 1:
    print("La ruta es ÓPTIMA")
else:
    print("La ruta NO es óptima")
