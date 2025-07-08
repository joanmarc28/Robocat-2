import socket
import psutil
import subprocess
import requests
import config
import os

# Comrpovar conexio a internet
def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Comprova si hi ha connexió a Internet.
    Per defecte intenta accedir al DNS de Google (8.8.8.8).
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"[ERROR] Connexió fallida: {ex}")
        return False

def get_session_token():
    try:
        res = requests.post(
            f"https://{config.SERVER_IP}/login",
            data={"email": config.ROBOCAT_USER, "password": config.ROBOCAT_PASSWORD}
        )
        if res.ok:
            print("🔓 Login correcte del Robocat.")
            return res.cookies.get("session")
        else:
            print(f"❌ Error al fer login del Robocat: {res.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Error en la connexió de login: {e}")
        return None

# Obtenir IP local
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Obtenir us de la CPU
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Obtenir us de la RAM
def get_ram():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent
    }

# Obtenir problemes de Sobreescalfament, baix voltatge o alt voltatge
def get_throttled_status():
    output = subprocess.check_output(['vcgencmd', 'get_throttled']).decode()
    return output.strip()

# Obtenir temperatura CPU
def get_cpu_temp():
    output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
    return float(output.replace("temp=", "").replace("'C\n", ""))

 # Obtenir frequencia CPU
def get_cpu_freq():
    output = subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']).decode()
    return int(output.split('=')[1]) / 1_000_000  # en MHz

def parse_throttled_state(hex_string):
    if '=' in hex_string:
        hex_value = int(hex_string.split('=')[1], 16)
    else:
        hex_value = int(hex_string, 16)

    def is_bit_set(value, bit):
        return (value & (1 << bit)) != 0

    state = {
        "under_voltage_now": is_bit_set(hex_value, 0),
        "frequency_capped_now": is_bit_set(hex_value, 1),
        "throttling_now": is_bit_set(hex_value, 2),
        "under_voltage_occurred": is_bit_set(hex_value, 16),
        "frequency_capped_occurred": is_bit_set(hex_value, 17),
        "throttling_occurred": is_bit_set(hex_value, 18),
    }
    return state

"""def print_throttled_status(status):
    for key, value in status.items():
        emoji = "🟢" if not value else "🔴"
        print(f"{emoji} {key.replace('_', ' ').capitalize()}: {'YES' if value else 'NO'}")
"""

def normalize_emocions(emocions: list[str]) -> list[str]:
    """Normalitza les etiquetes d'emocions retornades per Gemini.

    Es detecten variants i faltes d'ortografia comunes per tornar
    sempre un conjunt d'emocions canòniques com 'happy' o 'neutral'.
    """
    mapping = {
        "happy": ["happy", "felic", "feliz", "content", "alegre"],
        "angry": ["angry", "enfadat", "rabia", "furios", "enojat"],
        "sad": ["sad", "trist", "depressiu", "deprimit"],
        "surprised": ["surprised", "sorpres", "sorpresa", "astorat"],
        "scared": ["scared", "por", "espantat", "temor"],
        "disgusted": ["disgusted", "fastig", "asco", "asquejat"],
        "sleepy": ["sleepy", "adormit", "cansat", "son", "fatigat"],
        "default": ["neutral", "neutralitat", "netral", "sense emocio", "cap emocio"],
    }

    resultat = set()
    for emo in emocions:
        e = emo.lower().strip()
        trobat = False
        for canonic, variants in mapping.items():
            if any(e.startswith(v) or v in e for v in variants):
                resultat.add(canonic)
                trobat = True
                break
        if not trobat:
            resultat.add(e)
    return list(resultat)