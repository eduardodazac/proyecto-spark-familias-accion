# Importamos librerias necesarias 
from pyspark.sql import SparkSession, functions as F

# Inicializa la sesión de Spark 
spark = SparkSession.builder.appName('BatchFamiliasAccion').getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Define la ruta del archivo.csv en HDFS 
# Asegúrate que la ruta coincida con la creada en el Paso 2 de las instrucciones
file_path = 'hdfs://localhost:9000/Tarea_Familias/familias.csv'

print(f"Leyendo datos desde HDFS: {file_path}\n")

# Lee el archivo .csv 
# Usamos 'option("encoding", "UTF-8")' para manejar tildes y caracteres latinos
df = spark.read.format('csv') \
    .option('header', 'true') \
    .option('inferSchema', 'true') \
    .option('encoding', 'UTF-8') \
    .load(file_path)

# ----------------------------------------------------
# INICIO: Limpieza, Transformación y EDA
# ----------------------------------------------------

# Imprimimos el esquema 
print("Esquema del DataFrame:")
df.printSchema()

# Muestra las primeras 10 filas del DataFrame 
print("Muestra de datos:")
df.show(10)

# Análisis 1: Conteo de beneficiarios por Departamento
# (Usamos 'F.col' como en el Anexo 2 )
print("Conteo de beneficiarios por Departamento (Top 15):")
conteo_depto = df.groupBy("departamento") \
    .count() \
    .sort(F.col("count").desc())

conteo_depto.show(15)

# Análisis 2: Conteo de beneficiarios por Tipo de Pago
print("Conteo de beneficiarios por Tipo de Pago:")
conteo_pago = df.groupBy("tipo_pago") \
    .count() \
    .sort(F.col("count").desc())

conteo_pago.show()

# Análisis 3: Filtrar beneficiarios en un municipio específico (ej. BOGOTA D.C.)
print("Muestra de beneficiarios en 'BOGOTA D.C.':")
df_bogota = df.filter(F.col("municipio") == "BOGOTA D.C.") \
    .select("municipio", "tipo_pago", "estado_beneficiario")

df_bogota.show(10)

# ----------------------------------------------------
# FIN: Limpieza, Transformación y EDA
# ----------------------------------------------------

print("Análisis Batch completado.")
spark.stop()
