import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Obtener la lista de archivos CSV en la misma carpeta
carpeta = "CSVS"
archivos_csv = [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if archivo.endswith(".csv")]

# Lista para almacenar cada DataFrame
dataframes = []

# Leer cada archivo CSV y almacenar su contenido en la lista de DataFrames
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    dataframes.append(df)

resultados = pd.concat(dataframes, ignore_index=True)

# Eliminar filas con valores faltantes en goles_local y goles_visitante
resultados = resultados.dropna(subset=['goles_equipo_local', 'goles_equipo_visitante'])

# Dividir el conjunto de datos en características (X) y etiquetas (y)
X = resultados[['fase', 'equipo_local', 'equipo_visitante']]
y = resultados[['goles_equipo_local', 'goles_equipo_visitante']]

X = pd.get_dummies(X)

# Dividir datos en conjunto de entrenamiento y conjunto de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=50)

# Entrenar el modelo de Random Forest
modelo = RandomForestRegressor(n_estimators=100, random_state=50)
modelo.fit(X_train, y_train)

# Leer eliminatoria actual
octavos = pd.read_csv("Eliminatoria actual/eliminatoria.csv")

X_octavos = octavos[['fase', 'equipo_local', 'equipo_visitante']]
X_octavos_encoded = pd.get_dummies(X_octavos)

X_test_octavos = pd.DataFrame(columns=X_train.columns, data=np.zeros((X_octavos_encoded.shape[0], X_train.shape[1])))
for col in X_octavos_encoded.columns:
    if col in X_test_octavos.columns:
        X_test_octavos[col] = X_octavos_encoded[col]

predicciones = modelo.predict(X_test_octavos)

# Rellenar valores faltantes con las predicciones
octavos.loc[:, ['goles_equipo_local', 'goles_equipo_visitante']] = np.round(predicciones)

# Guardar datos actualizados en un nuevo archivo CSV
octavos.to_csv("resultado_octavos.csv", index=False)
