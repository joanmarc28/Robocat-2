import config
import speech_recognition as sr
import requests
import time
import difflib
import logging
from modes.agent import Agent
from movement.motors import mou_cap
import os
import threading
from interface.speaker import Speaker

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["ALSA_CARD"] = "default"
os.environ["SDL_AUDIODRIVER"] = "dsp"

class Micro:
    def __init__(self, agent: Agent = None, wake_word="hola", language="ca-ES",
                 device_index=None, debug=True, log_file="logs/micro.log"):
        self.agent = agent
        self.wake_word = wake_word.lower()
        self.language = language
        self.device_index = device_index
        self.recognizer = sr.Recognizer()
        self._running = True
        self.debug = debug

        # Logger setup
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self._setup_micro()

    def _setup_micro(self):
        # Si no s'ha especificat dispositiu, busca el primer amb canal d'entrada vàlid
        if self.device_index is None:
            try:
                for i, name in enumerate(sr.Microphone.list_microphone_names()):
                    with sr.Microphone(device_index=i) as source:
                        if source.CHUNK:
                            self.device_index = i
                            if self.debug:
                                print(f"🎙️ Micròfon detectat: {name} (index: {i})")
                            break
            except Exception as e:
                if self.debug:
                    print(f"[ERROR DETECCIÓ MICRO] {e}")
                return

        # Ajusta al soroll ambiental
        try:
            with sr.Microphone(device_index=self.device_index) as source:
                if self.debug:
                    print("🎙️ Ajustant al soroll ambiental...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.dynamic_energy_adjustment_ratio = 1.5
        except Exception as e:
            if self.debug:
                print(f"[ERROR CONFIGURACIÓ MICRO] {e}")

    def stop(self):
        self._running = False
        self.logger.info("Microphone stopped")

    def say(self, text):
        if self.agent and hasattr(self.agent, "speaker"):
            self.agent.speaker.say_text(text)
        elif self.debug:
            print(f"[SAY] {text}")
        self.logger.info(f"SAY: {text}")

    def send_to_gemini(self, text):
        url = f"https://{config.SERVER_IP}/chat"
        try:
            response = requests.post(url, json={"text": text})
            reply = response.json().get("response", None)
            self.logger.info(f"Gemini response: {reply}")
            return reply
        except Exception as e:
            if self.debug:
                print(f"[Gemini Error] {e}")
            return None

    def listen_once(self, timeout=6, phrase_time_limit=5):
        try:
            with sr.Microphone(device_index=self.device_index) as source:
                if self.debug:
                    print("🎧 Escoltant...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            result = self.recognizer.recognize_google(audio, language=self.language, show_all=True)

            if isinstance(result, dict) and "alternative" in result:
                text = result["alternative"][0].get("transcript", "").lower()
                self.logger.info(f"Escoltat: {text}")
                if self.debug:
                    print(f"[Escoltat] {text}")
                    for alt in result["alternative"]:
                        if "transcript" in alt:
                            print(f" - Possible: {alt['transcript']}")
                return text

            return None

        except sr.UnknownValueError:
            if self.debug:
                print("[Error] No s’ha entès cap veu.")
            return None
        except sr.RequestError as e:
            if self.debug:
                print(f"[Error Google API] {e}")
            return None
        except Exception as e:
            if self.debug:
                print(f"[Listen Error] {e}")
            return None


    def match_wake_word(self, text):
        ratio = difflib.SequenceMatcher(None, text, self.wake_word).ratio()
        if self.debug:
            print(f"[Similitud wake word] {ratio:.2f}")
        return ratio > 0.5  # Posa-ho més alt si vols més exigència

    def run(self,speak: Speaker = None):
        while self._running:
            if self.debug:
                print("👂 Listening for wake word...")
            self.logger.info("Listening for wake word")
            text = self.listen_once(timeout=6, phrase_time_limit=5)

            if text and self.match_wake_word(text):
                if self.debug:
                    print("✅ Wake word detectada!")
                self.logger.info("Wake word detected")

                #mou_cap()
                if self.agent:
                    self.agent.speaker.say_emotion("surprised")

                t_speak = threading.Thread(target=speak)
                t_speak.start()
                # Aquí pots activar Gemini si vols
                '''
                command = self.listen_once(timeout=7, phrase_time_limit=6)
                if command:
                    response = self.send_to_gemini(command)
                    print(f"Resposta de Gemini: {response}")
                    self.say(response or "Sorry, I didn't understand.")
                    if self.agent:
                        self.agent.handle_gemini_response(response or "")
                    else:
                        self.say("Can you repeat, please?")
                '''

            time.sleep(0.3)
