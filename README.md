# Proyecto: Análisis de Beneficiarios "Más Familias en Acción" 👨‍👩‍👧‍👦💰

Este proyecto implementa una solución de procesamiento de datos en batch y en tiempo real utilizando Apache Spark y Apache Kafka, siguiendo los lineamientos de los instructivos del curso de Big Data. El objetivo es analizar la distribución de los beneficiarios del programa "Más Familias en Acción" en Colombia.

## 1. Definición del Problema y Conjunto de Datos

* **Problema:** Analizar la distribución geográfica (batch) y los métodos de pago de los beneficiarios, y simular la inscripción de nuevos beneficiarios en tiempo real (streaming).
* **Conjunto de Datos:** Beneficiarios Más Familias en Acción.
* *Fuente:** Portal de Datos Abiertos de Colombia.
* **API del Dataset (CSV):** `https://www.datos.gov.co/resource/xfif-myr2.csv`

## 2. Descripción de la Solución

La solución se divide en dos partes, implementadas con Python y Spark:

### Procesamiento en Batch
1.  **Carga:** Se descargan los datos históricos desde la API de Datos Abiertos y se cargan en el sistema de archivos HDFS de Hadoop.
2.  **Análisis:** Un script de PySpark (`procesamiento_batch.py`) lee este CSV desde HDFS , infiere el esquema  y realiza un análisis exploratorio (EDA) para determinar el conteo de beneficiarios por departamento y tipo de pago.
3.  *Almacenamiento:** Los resultados del análisis se muestran en consola.

### Procesamiento en Tiempo Real (Spark Streaming & Kafka)
1.  **Productor de Kafka:** Un script (`productor_kafka.py`) simula la llegada de **nuevas inscripciones**. Genera datos aleatorios (ej. `{"municipio": "BOGOTA D.C.", "tipo_pago": "Giro"}`) y los envía a un topic de Kafka llamado `nuevos_beneficiarios`
2.  ]**Consumidor Spark Streaming:** Un script (`consumidor_streaming.py`) se conecta a Spark y se suscribe al topic de Kafka
3.  **Análisis:** Procesa los datos en micro-lotes, contando el número de nuevas inscripciones por municipio en ventanas de tiempo de 1 minuto
4.  **Visualización:** Muestra los resultados del conteo en tiempo real en la consola.

## 3. Instrucciones de Ejecución

Estas instrucciones asumen que ya tienes Hadoop, Spark y Kafka instalados y configurados en tu máquina virtual, como se detalla en los `Anexo 2` y `Anexo 3`.

### Prerrequisitos
* Máquina Virtual con Hadoop y Spark.
* Kafka instalado en `/opt/Kafka`.
* Bibliotecas de Python instaladas:
    ```bash
    sudo apt install -y python3-pip 
    sudo pip install pyspark 
    pip install kafka-python
    ```

### Paso 1: Clonar este Repositorio
```bash
git clone [https://github.com/tu-usuario/proyecto-spark-familias-accion.git](https://github.com/tu-usuario/proyecto-spark-familias-accion.git)
cd proyecto-spark-familias-accion
```

### Paso 2: Procesamiento Batch (Carga y Análisis)

Sigue los pasos del `Anexo 2` para cargar tus datos en HDFS.

1.  **Iniciar Hadoop** (en una terminal, como usuario `hadoop`):
    ```bash
    su - hadoop 
    start-all.sh
    ```

2.  **Preparar HDFS y Descargar Datos** (aún como usuario `hadoop`):
    * Crea la carpeta en HDFS:
        ```bash
        hdfs dfs -mkdir /Tarea_Familias 
        ```
    * Descarga el dataset (usamos `-O` para renombrarlo a `familias.csv`):
        ```bash
        wget [https://www.datos.gov.co/resource/xfif-myr2.csv](https://www.datos.gov.co/resource/xfif-myr2.csv) -O familias.csv [cite: 766]
        ```
    * Sube el archivo a HDFS:
        ```bash
        hdfs dfs -put /home/hadoop/familias.csv /Tarea_Familias [cite: 828, 853]
        ```
    * Verifica que el archivo esté en HDFS:
        ```bash
        hdfs dfs -ls /Tarea_Familias
        ```

3.  **Ejecutar el Script Batch** (en una **nueva** terminal de Putty, como usuario `vboxuser`):
    * Inicia el Spark Master y Worker:
        ```bash
        start-master.sh 
        start-worker.sh spark://bigdata:7077 
        ```
    * Navega a la carpeta del proyecto y ejecuta el script con `spark-submit`:
        ```bash
        cd proyecto-spark-familias-accion/
        spark-submit src/batch/procesamiento_batch.py
        ```
    * Verás la salida del análisis (esquema, conteo por departamento, etc.) en esta terminal.

### Paso 3: Procesamiento en Tiempo Real (Kafka y Streaming)

Sigue los pasos del `Anexo 3`. Necesitarás **dos terminales** adicionales (como usuario `vboxuser`).

1.  **Iniciar Zookeeper y Kafka** (en la Terminal 1, como `vboxuser`):
    * Inicia Zookeeper (en segundo plano):
        ```bash
        sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties & 
        ```
    * Inicia Kafka (en segundo plano):
        ```bash
        sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties & 
        ```
    * Crea el Topic (lo llamaremos `nuevos_beneficiarios`):
        ```bash
        /opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic nuevos_beneficiarios [cite: 1556]
        ```

2.  **Ejecutar el Consumidor Spark Streaming** (en la misma Terminal 1):
    * Ejecuta el script `consumidor_streaming.py` usando `spark-submit` con el paquete de Kafka:
        ```bash
        cd proyecto-spark-familias-accion/
        spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 src/streaming/consumidor_streaming.py
        ```
    * Esta terminal empezará a esperar datos.

3.  **Ejecutar el Productor de Kafka** (en la Terminal 2 ):
    * Ejecuta el script `productor_kafka.py`:
        ```bash
        cd proyecto-spark-familias-accion/
        python3 src/streaming/productor_kafka.py [cite: 1741]
        ```
    * Esta terminal mostrará los datos simulados que está enviando.

### Paso 4: Visualización de Resultados

* **Resultados Batch:** Aparecen en la consola donde ejecutaste `spark-submit src/batch/procesamiento_batch.py`.
* **Resultados Streaming:**
    * La **Terminal 1** (Consumidor) mostrará tablas de conteo que se actualizan cada minuto.
    * La **Terminal 2** (Productor) mostrará los JSON que se están enviando.
* **Interfaz Web de Spark:** Puedes monitorear los *Jobs* y *Stages* accediendo a la UI de Spark en tu navegador: `http://<IP_MAQUINA_VIRTUAL>:4040`
