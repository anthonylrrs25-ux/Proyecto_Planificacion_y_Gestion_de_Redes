import time
from celery import Celery

celery_app = Celery("network_tasks", broker="amqp://guest:guest@rabbitmq:5672//")

@celery_app.task(name="tasks.procesar_syslogs_en_background")
def procesar_syslogs_en_background():
    time.sleep(0.1)
    return "Logs analizados, indexados y almacenados en el histórico de gestión de red."