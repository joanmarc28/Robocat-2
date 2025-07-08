
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils.lk_tracker import *
from utils.homografia import *
from utils.show_keypoints import *

def load_video_as_numpy(path, max_frames=None):
    cap = cv2.VideoCapture(path)
    frames = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        count += 1
        if max_frames and count >= max_frames:
            break

    cap.release()
    return np.array(frames)  # Shape: (N, H, W, C)

def equal_number_kp(keypoints):
    lens = [len(kp) for kp in keypoints]
    max_len = np.min(lens)

    keypoints_np = np.zeros((len(keypoints),max_len,2))
    for i in range(len(keypoints)):
        for j in range(max_len):
            #print(i)
            keypoints_np[i,j,:] = keypoints[i][j]
    
    return keypoints_np

def make_video(video_array: np.ndarray, output_filename: str, fps: int = 30):
    """
    Guarda un video RGB en un archivo.

    Parámetros:
    - video_array: np.ndarray de forma (num_frames, height, width, 3), tipo uint8
    - output_filename: str, nombre del archivo de salida (ej. 'video.mp4')
    - fps: int, cuadros por segundo (default 30)
    """
    # Validación
    if not isinstance(video_array, np.ndarray):
        raise ValueError("video_array debe ser un arreglo de NumPy")
    if video_array.ndim != 4 or video_array.shape[-1] != 3:
        raise ValueError("video_array debe tener forma (frames, height, width, 3)")

    num_frames, height, width, _ = video_array.shape

    # Codificador y configuración de salida
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # o 'XVID' para .avi
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    for i in range(num_frames):
        frame = video_array[i]
        # Asegurarse de que el frame esté en formato BGR para OpenCV
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(bgr_frame)

    out.release()
    print(f"Video guardado como {output_filename}")

TRANSFORMATION_MODE = ["translation", "translation+rotation","translation+scale", "affine"]
TRACKING_MODE = ["lk","orb","sift"]

def stable(path, next_path):
    tic = time.time()


    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    video_np = load_video_as_numpy(path)
    vd = video_np
    keypoints, kf = track_keypoints_lk(video, max_corners=8, min_distance=10)
    kp = equal_number_kp(keypoints)
    video_aligned = align_video(vd, kp, key_frames=kf, mode=TRANSFORMATION_MODE[0])
    new_path = make_video(video_aligned, next_path, fps)
    
    toc = time.time()
    dt = toc - tic     
    print(f"temps: {dt:0.04f}s")


#stable(r"C:\Users\MartiArmengod\Downloads\VC_MAIN\VC-main\21_U\21_U.avi", r"C:\Users\MartiArmengod\Downloads\VC_MAIN\VC-main\21_U\21_NS.avi")

    


