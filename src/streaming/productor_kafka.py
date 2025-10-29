import time
import json
import random
from kafka import KafkaProducer 

# Lista de municipios y tipos de pago para simular
MUNICIPIOS = ["MEDELLIN", "CALI", "BARRANQUILLA", "CARTAGENA", "CUCUTA", "BUCARAMANGA"]
TIPOS_PAGO = ["Giro", "Bancarizado"]

def generar_nueva_inscripcion():
    """ Simula un nuevo beneficiario inscribiéndose. """
    return {
        "municipio": random.choice(MUNICIPIOS),
        "tipo_pago": random.choice(TIPOS_PAGO),
        "timestamp": int(time.time())
    }

# Creamos el Productor de Kafka 
productor = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8') 
)

# Definimos el topic (debe ser el mismo que creaste)
TOPIC_NAME = 'nuevos_beneficiarios'

print(f"Enviando mensajes al topic: {TOPIC_NAME}. Presiona Ctrl+C para detener.")

while True:
    try:
        data = generar_nueva_inscripcion()
        
        # Enviar datos al topic [cite: 1603]
        productor.send(TOPIC_NAME, value=data)
        
        print(f"Sent: {data}") [cite: 1604]
        
        # Esperar 2 segundos antes de enviar el siguiente
        time.sleep(2) [cite: 1605]
        
    except KeyboardInterrupt:
        print("\nDeteniendo productor.")
        break

productor.close()
