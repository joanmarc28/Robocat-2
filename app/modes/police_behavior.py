import config
import time
from vision.plate_detection import PlateDetection
import requests
import base64
from datetime import datetime
from interface.speaker import Speaker
import cv2
from vision.camera import RobotCamera
from interface.display import clear_displays, displays_show_frames

class PoliceBehavior:
    def __init__(self, speaker:Speaker, camera):
        self.speaker = speaker
        self.camera = camera
        self.detected_plates = []  # Llista d'últimes matrícules detectades
        self.max_plates_stored = 5  # Quantes últimes guardes
        self.similarity_threshold = 0.85  # Percentatge mínim de similitud per considerar-la la mateixa

    def plates_are_similar(self, plate1, plate2):
        """Compara dos textos de matrícula i calcula la similitud."""
        if len(plate1) != len(plate2):
            return False

        matches = sum(c1 == c2 for c1, c2 in zip(plate1, plate2))
        similarity = matches / len(plate1)
        return similarity >= self.similarity_threshold

    def detect_license_plate(self, state="patrol", duration=3):

        t_inici = time.time()
        while time.time() - t_inici < duration:
            displays_show_frames(state)
        try:
            frame = self.camera.capture()
            car, car_box = PlateDetection.detect_car(frame, camera=self.camera)
            if car is None:
                return None

            plate, _ = PlateDetection.detect_plate(car, car_bbox=car_box, camera=self.camera)
            if plate is not None:
                data = self.reportar_infraccio()
                plate_text = data.get('matricules', [None])[0] if data else None

                for previous_plate in self.detected_plates:
                    if self.plates_are_similar(plate_text, previous_plate):
                        print(f"[POLICE] Matrícula similar detectada ({plate_text}), s'ignora la detecció.")
                        return None

                print(f"[POLICE] Nova matrícula detectada: {plate_text}")
                self.detected_plates.append(plate_text)
                if len(self.detected_plates) > self.max_plates_stored:
                    self.detected_plates.pop(0)
                return plate_text
            return None
        except Exception as e:
            print(f"[ERROR] Error en la detecció de matrícula: {e}")
            return None
        

    def reportar_infraccio(self):
        """Envia una imatge a la web per detectar infracció i guardar-la si s’escau."""
        frame = self.camera.capture()
        _, jpeg = cv2.imencode(".jpg", frame)
        image_base64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")

        try:
            res = requests.post(
                f"https://{config.SERVER_IP}/api/deteccio-frame",
                json={
                    "imatge": f"data:image/jpeg;base64,{image_base64}",
                    "mode": "infraccio"
                }
                #cookies={"session": config.SESSION_TOKEN}  # ← assegura’t que tens la cookie d’autenticació
            )
            if res.ok:
                data = res.json()
                print(data)
                print(f"[POLICE] 📸 Matrícules: {data.get('matricules', [])}")
                print(f"[POLICE] 🚫 Infracció: {data.get('infraccio', 'Cap')}")
                return data
            else:
                print(f"[ERROR] No sha pogut reportar la infracció: {res.status_code} - {res.text}")
                return None
        except Exception as e:
            print(f"[ERROR] Fallo reportant la infracció: {e}")
            return None

