import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Dataset simulado del transporte masivo de Bogotá
data = {
    "distancia_km": [8, 10, 15, 20, 7, 18, 9],
    "tiempo_min": [30, 40, 70, 90, 25, 80, 35],
    "num_transbordos": [0, 1, 3, 4, 0, 3, 1],
    "hora_pico": [0, 0, 1, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

# Normalización de datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Modelo K-Means
kmeans = KMeans(n_clusters=2, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

# Mostrar resultados
print("Agrupamiento de rutas:\n")
print(df)
