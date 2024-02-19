import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import mlflow
import mlflow.sklearn
from sklearn.preprocessing import StandardScaler

# Leer el primer CSV
df_stats = pd.read_csv('CSVS STATS/todas_stats.csv')

# Preprocesamiento de datos
# ... (manejar valores faltantes, convertir variables, etc.)
# Definir las variables features y target
features = df_stats[['victorias_esta_temp', 'empates_esta_temp', 'derrotas_esta_temp', 'porcentaje_victorias_esta_temp', 'porcentaje_empates_esta_temp', 'porcentaje_derrotas_esta_temp']]
target = df_stats['goles_equipo_local','goles_equipo_visitante']  # Asegúrate de reemplazar 'resultado_real' con el nombre correcto de tu columna objetivo en el conjunto de entrenamiento

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Inicializar MLFlow
mlflow.start_run()

# Entrenar el modelo
with mlflow.start_run():
    # Crear y entrenar el modelo (usar el algoritmo apropiado)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Guardar el modelo con MLFlow
    mlflow.sklearn.log_model(model, "model")

# Realizar predicciones en los datos del segundo CSV
df_octavos = pd.read_csv('Eliminatoria actual/eliminatoria.csv')

def preprocess_data(df):
    # Realizar las operaciones de preprocesamiento aquí
    # Ejemplo:

    # Manejo de valores faltantes (rellenar con cero en este caso)
    df.fillna(0, inplace=True)

    # Codificación de variables categóricas (si es necesario)
    # Por ejemplo, utilizando one-hot encoding
    df = pd.get_dummies(df, columns=['equipo_local', 'equipo_visitante'])

    # Normalización/escalamiento de características
    scaler = StandardScaler()
    df[['goles_equipo_local', 'goles_equipo_visitante']] = scaler.fit_transform(df[['goles_equipo_local', 'goles_equipo_visitante']])

    # Puedes agregar más operaciones según tus necesidades

    # Devolver los datos preprocesados
    return df
X_octavos = preprocess_data(df_octavos)

# Cargar el modelo guardado
loaded_model = mlflow.sklearn.load_model("runs:/<RUN_ID>/model")

# Realizar predicciones
predictions = loaded_model.predict(X_octavos)

# Agregar las predicciones al DataFrame original de octavos de final
df_octavos['resultado_predicho'] = predictions

# Imprimir el DataFrame con las predicciones
print(df_octavos[['equipo_local', 'equipo_visitante', 'resultado_predicho']])
mlflow.end_run()
