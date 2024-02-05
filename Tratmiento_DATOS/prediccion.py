import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.calibration import CalibratedClassifierCV

# Cargar los datasets
df_partidos = pd.read_csv('tudataset_partidos.csv')  # Asegúrate de tener el archivo correcto con las columnas adecuadas

# Crear columna de diferencia de puntajes y ventaja del equipo local
df_partidos['diferencia_puntajes'] = df_partidos['puntaje_local'] - df_partidos['puntaje_visitante']
df_partidos['ventaja_local'] = 3  # Puedes ajustar este valor según tu preferencia de ventaja local

# Seleccionar las características (features) y la variable objetivo (target)
X = df_partidos[['diferencia_puntajes', 'ventaja_local']]
y = df_partidos['resultado']  # 'resultado' debe ser una columna con etiquetas (0 para visitante gana, 1 para empate, 2 para local gana)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalar las características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Crear y entrenar el modelo de regresión logística
modelo = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
modelo_calibrado = CalibratedClassifierCV(modelo, method='sigmoid', cv='prefit')
modelo_calibrado.fit(X_train_scaled, y_train)

# Realizar predicciones en el conjunto de prueba
predicciones_proba = modelo_calibrado.predict_proba(X_test_scaled)

# Obtener las probabilidades de victoria para cada equipo y empate
probabilidad_visitante = predicciones_proba[:, 0]
probabilidad_empate = predicciones_proba[:, 1]
probabilidad_local = predicciones_proba[:, 2]

# Mostrar las probabilidades
resultados = pd.DataFrame({
    'Probabilidad_Visitante': probabilidad_visitante,
    'Probabilidad_Empate': probabilidad_empate,
    'Probabilidad_Local': probabilidad_local,
    'Resultado_Real': y_test
})

print(resultados)

# Puedes ajustar el umbral para determinar la predicción final (por ejemplo, si Probabilidad_Local > 0.5 entonces predecir que el equipo local ganará)
