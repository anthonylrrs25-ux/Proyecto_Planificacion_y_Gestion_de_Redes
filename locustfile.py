from locust import HttpUser, task, between

class AuditorRedUser(HttpUser):
    # Tiempo de espera entre ráfagas de tráfico simulado de red
    wait_time = between(0.1, 0.5)

    @task(3)
    def consultar_inventario(self):
        """Simula administradores de red consultando los dispositivos concurrentemente"""
        self.client.get("/")

    @task(1)
    def simular_trafico_syslog_pesado(self):
        """Simula ráfagas de eventos syslog bloqueando el servidor de forma síncrona"""
        self.client.get("/heavy")

    @task(1)
    def simular_trafico_syslog_optimizado(self):
        """Simula eventos syslog gestionados por la arquitectura de colas (Opcional)"""
        self.client.get("/queue")