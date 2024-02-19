import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import mlflow
import mlflow.sklearn

# Leer el CSV de estadísticas
df_stats = pd.read_csv('CSVS STATS/todas_stats.csv')

# Definir 'features' y 'target'
features = df_stats.drop(['Golesxpartido Local_ult10_temp', 'Golesxpartido Visitante_ult10_temp'], axis=1)
target = df_stats[['Golesxpartido Local_ult10_temp', 'Golesxpartido Visitante_ult10_temp']]

# Separar las columnas numéricas y categóricas
numeric_features = features.select_dtypes(include=['float64']).columns
categorical_features = features.select_dtypes(include=['object']).columns

# Crear transformers para columnas numéricas y categóricas
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore')),
])

# Crear preprocessor que maneja ambas transformaciones
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
    ])

# Crear el pipeline con el preprocessor y el modelo RandomForestRegressor
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("RandomForest")
# Inicializar MLFlow
mlflow.start_run()

# Entrenar el modelo
with mlflow.start_run(nested=True, run_name="Entrenamiento del modelo"):
    # Entrenar el modelo con el pipeline
    model.fit(X_train, y_train)

    # Guardar el modelo con MLFlow
    mlflow.sklearn.log_model(model, "random_forest_model")

    # Obtener el ID de la ejecución actual
    run_id = mlflow.active_run().info.run_id
    print(f"ID de la ejecución actual: {run_id}")

# Cargar el modelo guardado
loaded_model = mlflow.sklearn.load_model(f"runs:/{run_id}/random_forest_model")

# Evaluar el modelo en el conjunto de prueba
test_predictions = loaded_model.predict(X_test)
# Puedes agregar más métricas de evaluación según tus necesidades

# Imprimir el resultado de la evaluación
print("Evaluación en el conjunto de prueba:")
print(test_predictions)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("MAE:", mean_absolute_error(y_test, test_predictions))
print("MSE:", mean_squared_error(y_test, test_predictions))
print("R-squared:", r2_score(y_test, test_predictions))

import matplotlib.pyplot as plt

plt.scatter(y_test, test_predictions)
plt.xlabel("Observaciones reales")
plt.ylabel("Predicciones")
plt.title("Predicciones vs. Observaciones reales")
plt.show()

