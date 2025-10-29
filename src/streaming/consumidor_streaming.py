from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# --- Configuración de la Sesión de Spark ---
spark = SparkSession.builder \
    .appName("StreamingFamiliasAccion") \
    .getOrCreate()

# Reducir el nivel de log para limpiar la salida
spark.sparkContext.setLogLevel("WARN")

# --- Definición del Esquema ---
# El esquema debe coincidir con los datos JSON del productor
schema = StructType([
    StructField("municipio", StringType()),
    StructField("tipo_pago", StringType()),
    StructField("timestamp", TimestampType())
]) # Adaptado para el nuevo JSON

# --- Lectura del Stream de Kafka ---
df_kafka = spark \
    .readStream \
    .format("kafka") 
    .option("kafka.bootstrap.servers", "localhost:9092") 
    .option("subscribe", "nuevos_beneficiarios")
    .load()

# --- Transformación de Datos ---
# Convertir el 'value' de Kafka (binario) a String y luego a JSON
parsed_df = df_kafka.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*") 

# --- Análisis en Tiempo Real: Conteo por Ventana ---
# Contar inscripciones por municipio en ventanas de 1 minuto
windowed_counts = parsed_df \
    .groupBy(
        window(col("timestamp"), "1 minute"), 
        col("municipio")
    ) \
    .count() \
    .orderBy(col("window").desc(), col("count").desc())

# --- Salida a Consola ---
# Mostrar los resultados en la consola 
query = windowed_counts \
    .writeStream \
    .outputMode("complete")  \
    .format("console")  \
    .option("truncate", "false") \
    .start() 

print("Esperando datos del stream de Kafka... (topic: nuevos_beneficiarios)")
query.awaitTermination()
