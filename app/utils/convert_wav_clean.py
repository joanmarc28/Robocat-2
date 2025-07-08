import os
import subprocess

INPUT_FOLDER = "../assets/sounds"
OUTPUT_FOLDER = "../assets/sounds_clean"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".wav"):
        name, _ = os.path.splitext(filename)
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, f"{name}_clean.wav")

        print(f"🎧 Convertint {filename}...")

        command = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ac", "2",              # 2 canals (estèreo)
            "-ar", "44100",          # 44.1 kHz
            "-sample_fmt", "s16",    # 16-bit
            output_path
        ]

        subprocess.run(command, check=True)

print("✅ Conversió completada.")
