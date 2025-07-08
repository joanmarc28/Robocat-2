import time
from modes.human_behavior import HumanBehavior
from modes.police_behavior import PoliceBehavior
from interface.speaker import Speaker
from vision.camera import RobotCamera
import config
from movement.motors import mou_cap
import threading

class Agent:
    def __init__(self, camera:RobotCamera= None, speaker:Speaker= None, time=0.1,frenquencia=5):
        self.mode = config.DEFAULT_MODE
        self.submode = "default"
        self.speaker = speaker
        self.camera = camera
        self.time = time
        self.frequencia = frenquencia
        self.human = HumanBehavior(self.speaker, self.camera)
        self.police = PoliceBehavior(self.speaker, self.camera)

        self.running = True
        self.last_action_time = 0

    def set_mode(self, mode):
        if mode in ["human", "police"]:
            print(f"Mode ➜ {mode}")
            self.mode = mode
            self.submode = "default"
        else:
            print(f"Mode desconegut: {mode}")

    def set_submode(self, submode):
        print(f"Submode ➜ {submode}")
        self.submode = submode

    def run(self):
        print("Agent en execució...")
        while self.running:
            now = time.time()

            # Limita la freqüència d'acció (ex: cada 5s)
            if now - self.last_action_time >= self.frequencia:

                self.last_action_time = now

                def speak():
                    self.speaker.say_emotion(self.submode)

                t_speak = threading.Thread(target=speak)
                t_speak.start()
                t_speak.join()

                self._execute_mode()
         
            if self.mode == "human":
                self.time = 0.1  # Més ràpid per a interaccions humanes
                self.frequencia = 5  # Accions humanes més freqüents
            elif self.mode == "police":
                self.time = 0.1  # Més lent per a accions policials
                self.frequencia = 10  # Accions policials menys freqüents

            time.sleep(self.time)  # Redueix ús de CPU

    def stop(self):
        print("Aturant Agent")
        self.running = False

    def _execute_mode(self):
        print(f"Executant: mode={self.mode}, submode={self.submode}")
        if self.mode == "human":
            self.human.express_emotion(self.submode)
            emocions,analisis = self.human.analitza_emocions()
            self.human.process_emocions(emocions)
        elif self.mode == "police":
            if self.submode == "default":
                self.police.detect_license_plate()
            else:
                print(f"Submode policial desconegut: {self.submode}")

