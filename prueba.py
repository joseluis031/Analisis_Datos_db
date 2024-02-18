import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import mlflow
import mlflow.sklearn

# Leer el primer CSV
df_stats = pd.read_csv('CSVS STATS/todas_stats.csv')

# Leer el segundo CSV
df_octavos = pd.read_csv('Eliminatoria actual/eliminatoria.csv')

# Definir 'features' y 'target'
features = df_stats[['porcentaje_victorias_ult10_temp', 'porcentaje_empates_ult10_temp', 'porcentaje_derrotas_ult10_temp', 'Golesxpartido Local_ult10_temp', 'Golesxpartido Visitante_ult10_temp']]
target = df_stats[['Golesxpartido Local_ult10_temp', 'Golesxpartido Visitante_ult10_temp']]

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Inicializar MLFlow
mlflow.start_run()

# Entrenar el modelo
with mlflow.start_run(nested=True, run_name="Entrenamiento del modelo"):
    # Crear y entrenar el modelo (usar el algoritmo apropiado)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Guardar el modelo con MLFlow
    mlflow.sklearn.log_model(model, "model")

    # Obtener el ID de la ejecución actual
    run_id = mlflow.active_run().info.run_id
    print(f"ID de la ejecución actual: {run_id}")

# Cargar el modelo guardado
loaded_model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

# Realizar predicciones en los datos del segundo CSV
X_octavos = df_octavos[['porcentaje_victorias_ult10_temp', 'porcentaje_empates_ult10_temp', 'porcentaje_derrotas_ult10_temp', 'Golesxpartido Local_ult10_temp', 'Golesxpartido Visitante_ult10_temp']]
predictions = loaded_model.predict(X_octavos)

# Agregar las predicciones al DataFrame original de octavos de final
df_octavos['goles_predichos_local'] = predictions[:, 0]
df_octavos['goles_predichos_visitante'] = predictions[:, 1]

# Imprimir el DataFrame con las predicciones
print(df_octavos[['equipo_local', 'equipo_visitante', 'goles_predichos_local', 'goles_predichos_visitante']])
