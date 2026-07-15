from fastapi import FastAPI
import time
from celery import Celery
from prometheus_client import make_asgi_app, Counter, Histogram

app = FastAPI(title="API de Gestión de Redes - Universidad de Guayaquil")

# Configuración del Broker de Mensajería para desacoplamiento (Opcional)
celery_app = Celery("network_tasks", broker="amqp://guest:guest@rabbitmq:5672//")

# Métricas de rendimiento para Prometheus
REQUEST_COUNT = Counter(
    "network_api_requests_total", "Total de peticiones en la API de Redes", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "network_api_duration_seconds", "Tiempo de respuesta de la infraestructura en segundos", ["endpoint"]
)

# Endpoint global de métricas para el raspado de Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Base de datos simulada de la infraestructura de red
INVENTARIO_RED = {
    "switches_core": ["SW-Guayaquil-Core01", "SW-Guayaquil-Core02"],
    "routers_bgp": ["RTR-UG-BGP01", "RTR-UG-BGP02"],
    "firewalls": ["FW-UG-Asa5516"],
    "vlans_configuradas": [10, 20, 30, 40, 99]
}

@app.get("/")
async def get_network_inventory():
    """Consulta rápida del estado e inventario de los dispositivos de red"""
    start_time = time.time()
    
    # Registro de métricas
    REQUEST_COUNT.labels(method="GET", endpoint="/", http_status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start_time)
    
    return {
        "status": "online",
        "modulo": "Gestión de Inventario de Red",
        "data": INVENTARIO_RED
    }

@app.get("/heavy")
async def process_syslogs_sync():
    """Simula el procesamiento SÍNCRONO de ráfagas de logs (Syslog) del Firewall"""
    start_time = time.time()
    
    # Simula el procesamiento pesado en CPU al parsear texto de logs de red
    time.sleep(0.1) 
    
    REQUEST_COUNT.labels(method="GET", endpoint="/heavy", http_status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/heavy").observe(time.time() - start_time)
    
    return {
        "status": "processed",
        "modulo": "Analizador de Syslogs Integrado",
        "logs_analizados": 1500,
        "alerta": "Se detectaron múltiples intentos de escaneo de puertos (Port Scanning) en la VLAN 10"
    }

@app.get("/queue")
async def process_syslogs_async():
    """PUNTO OPCIONAL: Desacopla el procesamiento de Syslogs enviándolo a RabbitMQ"""
    start_time = time.time()
    
    # Delegamos la tarea de red al worker de Celery de forma asíncrona
    celery_app.send_task("tasks.procesar_syslogs_en_background")
    
    REQUEST_COUNT.labels(method="GET", endpoint="/queue", http_status="202").inc()
    REQUEST_LATENCY.labels(endpoint="/queue").observe(time.time() - start_time)
    
    return {
        "status": "enqueued",
        "modulo": "Gestión de Colas de Red (RabbitMQ)",
        "message": "Lote de Syslogs enviado exitosamente al Broker de mensajería para procesamiento asíncrono"
    }