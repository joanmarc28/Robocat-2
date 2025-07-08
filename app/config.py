# config.py
from utils.secret import user_password

ROBOT_ID = "robocat001"  # ID percada robot
SERVER_IP = "robocat.jmprojects.cat"  # IP del servidor web

ROBOCAT_USER = "robocat@robocat.cat"
ROBOCAT_PASSWORD = user_password()
SESSION_TOKEN = None

# I2C pins 
I2C_BUS_OLED_LEFT = 3
I2C_BUS_OLED_RIGHT = 4
I2C_BUS_GPS = 5

# Pins Ultrasons
ULTRASONIC_TRIG = 8
ULTRASONIC_ECHO = 23
LLINDAR_ULTRASONIC = 10  # Distància mínima per l'alerta d'aproximació

# Pantalla OLED
OLED_WIDTH = 128
OLED_HEIGHT = 64
EYE_DELAY = 0.01

# Configuració de la càmera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
CAMERA_ROTATE = 0  # Rotació de la càmera en graus (0, 90, 180, 270)
CAMERA_FLIP = False  # Inverteix la imatge horitzontalment

# Mode de funcionament per defecte
DEFAULT_MODE = "police"

SOUNDS_DIR = "assets/sounds_clean"
AUDIO_DEVICE = "plughw:1,0"

STATES = {"default":{
            "sounds": ["purr_1_clean.wav"],
            "eyes":""
        }, 
        "happy":{
            "sounds": ["cute_1_clean.wav"],
        },  
        "patrol":{
            "sounds": ["angry_2_clean.wav"],
        },  
        "angry":{
            "sounds": ["angry_1_clean.wav"],
        },    
        "surprised":{
            "sounds": ["funny_1_clean.wav"],
        },     
        "sleepy":{
            "sounds": ["purr_1_clean.wav"],
        },  
        "sad":{
            "sounds": ["sad_1_clean.wav"],
        },
        "scared":{
            "sounds": ["sad_1_clean.wav"],
        },
        "disgusted":{
            "sounds": ["sick_1_clean.wav"],
    }
}
