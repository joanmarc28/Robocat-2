import cv2
import numpy as np
import time
#from utils.show_keypoints import *
#from show_keypoints import *


def track_keypoints_sift(
    video,
    nfeatures=300,
    nOctaveLayers=3,
    contrastThreshold=0.04,
    edgeThreshold=10,
    sigma=1.6
):
    """
    Fa el tracking de punts clau mitjançant SIFT.

    Paràmetres:
    - video: objecte cv2.VideoCapture
    - nfeatures: nombre màxim de punts que es volen mantenir (0 = sense límit)
    - nOctaveLayers: nombre de subdivisions per octava (per defecte 3)
    - contrastThreshold: llindar per eliminar punts de contrast baix (per defecte 0.04)
    - edgeThreshold: llindar per descartar punts prop de les vores (per defecte 10)
    - sigma: valor inicial del blur Gaussià (per defecte 1.6)

    """

    if not video.isOpened():
        print("Error: no s'ha pogut obrir el vídeo.")
        return [], 0

    ret, old_frame = video.read()
    if not ret:
        print("Error: no s'ha pogut llegir el primer fotograma.")
        return [], 0

    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    # Inicialitza SIFT amb els paràmetres especificats
    sift = cv2.SIFT_create(
        nfeatures=nfeatures,
        nOctaveLayers=nOctaveLayers,
        contrastThreshold=contrastThreshold,
        edgeThreshold=edgeThreshold,
        sigma=sigma
    )

    # Detecta punts al primer frame
    kp, des = sift.detectAndCompute(old_gray, None)
    keypoints_tracked = [np.array([kp[i].pt for i in range(len(kp))])]

    frame_idx = 1
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    while frame_idx <= frame_count:
        ret, frame = video.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp, des = sift.detectAndCompute(frame_gray, None)
        keypoints_tracked.append(np.array([kp[i].pt for i in range(len(kp))]))

        frame_idx += 1

    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    return keypoints_tracked, [0, frame_idx]



if __name__ == '__main__':
    video = cv2.VideoCapture("video/21_stable.avi")
    keypoints, _ = track_keypoints_sift(video, nfeatures=300)
    mostrar_punts(video, keypoints)
    video.release()

    print(f"Punts seguits en {len(keypoints)} frames.")
