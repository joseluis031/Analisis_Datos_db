from pyspark.sql import SparkSession

# Crea una sesión de Spark
spark = SparkSession.builder.appName("ejemplo_csv").getOrCreate()

# Ruta al archivo CSV
archivo_csv = "CSVS/temp2019_20.csv"

# Lee el archivo CSV en un DataFrame de Spark
dataframe = spark.read.csv(archivo_csv, header=True, inferSchema=True)

# Muestra el contenido del DataFrame
dataframe.show()

# Puedes realizar operaciones adicionales en el DataFrame según tus necesidades
# Por ejemplo, puedes filtrar, agrupar, realizar transformaciones, etc.

# Cierra la sesión de Spark al finalizar
spark.stop()
