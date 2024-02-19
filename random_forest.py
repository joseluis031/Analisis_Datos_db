import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
import os
# Cargar los CSVs
carpeta_csvs = 'CSVS'

# Lista para almacenar los DataFrames
dfs = []

# Leer y combinar los CSVs
for archivo in os.listdir(carpeta_csvs):
    if archivo.endswith(".csv"):
        ruta_csv = os.path.join(carpeta_csvs, archivo)
        dfs.append(pd.read_csv(ruta_csv))

df_combinado = pd.concat(dfs, ignore_index=True)

# Crear la columna 'resultado'
df_combinado['resultado'] = df_combinado.apply(lambda row: 1 if row['goles_equipo_local'] > row['goles_equipo_visitante'] else (0 if row['goles_equipo_local'] == row['goles_equipo_visitante'] else 2), axis=1)

# Lidiar con los valores faltantes
df_combinado = df_combinado.fillna(method='ffill')

# Definir las variables 'features' y 'target'
features = df_combinado[['goles_equipo_local', 'goles_equipo_visitante']]
target = df_combinado['resultado']

# Definir el modelo de regresión logística
model = LogisticRegression()

# Definir el número de folds
k_folds = 5

# Evaluar el modelo usando K-Fold Cross Validation
scores = cross_val_score(model, features, target, cv=KFold(n_splits=k_folds, shuffle=True))

# Imprimir la precisión promedio
print("Precisión promedio:", scores.mean())

# Ajustar el hiperparámetro C
model = LogisticRegression(C=1.0)

# Evaluar el modelo usando K-Fold Cross Validation
scores = cross_val_score(model, features, target, cv=KFold(n_splits=k_folds, shuffle=True))

# Imprimir la precisión promedio
print("Precisión promedio con C=1.0:", scores.mean())