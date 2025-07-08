import RPi.GPIO as GPIO
import time
import config
from telemetria_shared import telemetria_data

class ModulUltrasons:
    """Classe per gestionar les potes del quadrúpede."""
    def __init__(self):
        # Configura els pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.ULTRASONIC_TRIG, GPIO.OUT)
        GPIO.setup(config.ULTRASONIC_ECHO, GPIO.IN)

    def mesura_distancia(self):
        # Envia trigger curtet
        GPIO.output(config.ULTRASONIC_TRIG, False)
        time.sleep(0.0002)
        GPIO.output(config.ULTRASONIC_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(config.ULTRASONIC_TRIG, False)

        # Espera l'eco
        # Espera l'eco amb timeout per evitar bloquejos
        timeout = 0.02  # 20 ms
        start_time = time.time()

        start = start_time
        while GPIO.input(config.ULTRASONIC_ECHO) == 0 and (time.time() - start_time) < timeout:
             start = time.time()

        if (time.time() - start_time) >= timeout:
            return None

        start_time = time.time()
        end = start_time
        while GPIO.input(config.ULTRASONIC_ECHO) == 1 and (time.time() - start_time) < timeout:
             end = time.time()
             
        if (time.time() - start_time) >= timeout:
            return None

        # Calcula temps i distancia
        duration = end - start
        distance = (duration * 34300) / 2  # velocitat so = 34300 cm/s

        return distance
    
    def mesura_distancia_auto(self):
        dist = self.mesura_distancia()
        print(f"Distància: {dist:.2f} cm")

    def thread_ultrasons(self):
        while True:
            """ultrasons.mesura_distancia_auto()"""
            try:
                dist = self.mesura_distancia()
                if dist is not None:
                    telemetria_data["dist"] = dist
            except Exception as e:
                print(f"[ERROR] Ultrasons: {e}")
            time.sleep(0.5)

