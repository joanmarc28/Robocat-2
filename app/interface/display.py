# interface/display.py
from PIL import Image, ImageDraw
import board
import busio
import config
import os
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import ImageFont
import threading

class Display:
    """Classe per gestionar displays"""
    def __init__(self,width=config.OLED_WIDTH, height=config.OLED_HEIGHT, bus=None, address=0x3C):
        self.serial2 = i2c(port=bus, address=address)
        self.display = ssd1306(self.serial2, width=width, height=height)
        self.image = Image.new("1", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.width = width
        self.height = height
        self.max_lines = height // 10
        self.line_cache = []


        # Escull la font: predeterminada o TTF
        # self.font = ImageFont.load_default()
        self.font = ImageFont.truetype("assets/fonts/PressStart2P.ttf", 6)  # exemple

        # Càlcul segur de l'alçada de línia
        """       bbox = self.font.getbbox("A")
        self.line_height = bbox[3] - bbox[1]
        self.max_lines = height // self.line_height"""

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.display.display(self.image)    

    def display_message(self,text):

        # Afegeix la nova línia al final
        self.line_cache.append(text)

        # Si tenim més línies del que cap, elimina les més antigues
        if len(self.line_cache) > self.max_lines:
            self.line_cache = self.line_cache[-self.max_lines:]

        # Esborra la imatge
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Escriu totes les línies del buffer
        for i, line in enumerate(self.line_cache):
            y = i * 10
            self.draw.text((0, y), line,font=self.font, fill=255)

        # Actualitza les dues pantalles
        self.display.display(self.image)

    def show_frames(self,carpeta_frames,side="left",eye_delay=config.EYE_DELAY):
        # Llegeix i ordena els fitxers de la carpeta
        fitxers = sorted([
            f for f in os.listdir("assets/eyes_img/"+carpeta_frames+"/"+side)
            if f.lower().endswith(('.png', '.bmp'))
        ])

        if not fitxers:
            print("No s'han trobat imatges a la carpeta.")
            return

        #print(f"Mostrant {len(fitxers)} frames...")

        for nom_fitxer in fitxers:
            ruta = os.path.join("assets/eyes_img/"+carpeta_frames+"/"+side, nom_fitxer)
            #print(f"{nom_fitxer}")

            # Obre i redimensiona la imatge si cal
            imatge = Image.open(ruta).convert("1").resize((self.width, self.height))
            self.display.display(imatge)
            time.sleep(eye_delay)

display_right = None
display_left = None

def start_displays():
    """Inicialitza les pantalles OLED"""
    global display_right, display_left
    errors = True
    try:
        display_right = Display(width=config.OLED_WIDTH, height=config.OLED_HEIGHT, bus=config.I2C_BUS_OLED_RIGHT)
    except Exception as e:
        print(f"[ERROR] Dreta Displays: {e}")
        errors = False
    try:
        display_left = Display(width=config.OLED_WIDTH, height=config.OLED_HEIGHT, bus=config.I2C_BUS_OLED_LEFT)
    except Exception as e:
        print(f"[ERROR] EsquerraDisplays: {e}")
        errors = False
    return errors

def clear_displays():
    if display_left is None or display_right is None:
        print("No es pot Netejar les pantalles, no estan inicialitzades")
        return
    display_left.clear()
    display_right.clear()

def displays_message(text):
    """Mostra un missatge a les pantalles OLED"""
    if display_left is None or display_right is None:
        print(text)
        return
    display_left.display_message(text)
    display_right.display_message(text)

def displays_show_frames(carpeta_frames, eye_delay=config.EYE_DELAY):
    if display_left is not None and display_right is not None:
        # Crear i iniciar els fils per cada pantalla
        thread_left = threading.Thread(target=display_left.show_frames, args=(carpeta_frames, "left", eye_delay), daemon=True)
        thread_right = threading.Thread(target=display_right.show_frames, args=(carpeta_frames, "right", eye_delay), daemon=True)

        thread_left.start()
        thread_right.start()

        # Si vols esperar que acabin abans de continuar:
        thread_left.join()
        thread_right.join()
    elif display_left is not None:
        display_left.show_frames(carpeta_frames, "left", eye_delay)
    elif display_right is not None:
        display_right.show_frames(carpeta_frames, "right", eye_delay)
    else:
        return