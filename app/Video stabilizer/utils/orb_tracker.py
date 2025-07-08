import cv2
import numpy as np
import time

#from utils.show_keypoints import *
#from show_keypoints import *


import cv2
import numpy as np
import time

#from utils.show_keypoints import *
#from show_keypoints import *


def track_keypoints_orb(
    video,
    nfeatures=300,
    scaleFactor=1.2,
    nlevels=8,
    edgeThreshold=31,
    fastThreshold=20
):
    """
    Fa el tracking de punts clau mitjançant ORB.

    Paràmetres:
    - video: objecte cv2.VideoCapture
    - nfeatures: nombre màxim de keypoints 
    - scaleFactor: factor de reducció entre nivells de la piràmide 
    - nlevels: nivells de la piràmide d'escala 
    - edgeThreshold: marge exclòs per detectar keypoints 
    - fastThreshold: llindar per al detector FAST 
    """

    # Mirar si esta obert
    assert video.isOpened(), "Error: no s'ha pogut obrir el vídeo."
    
    # Mirar si te frames
    ret, old_frame = video.read()
    assert ret, "Error: no s'ha pogut obrir el vídeo."
    
    # Inicialitza ORB amb els paràmetres especificats
    orb = cv2.ORB_create(
        nfeatures=nfeatures,
        scaleFactor=scaleFactor,
        nlevels=nlevels,
        edgeThreshold=edgeThreshold,
        fastThreshold=fastThreshold
    )

    # Detecta punts al primer frame
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    kp, _ = orb.detectAndCompute(old_gray, None)
    keypoints_tracked = [np.array([kp[i].pt for i in range(len(kp))])]


    # iterem per els frames indicats
    frame_idx = 1
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    while frame_idx < frame_count:

        # Comprovem si hi ha frames
        ret, frame = video.read()
        if not ret:
            break

        # Detectem punts al frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp, _ = orb.detectAndCompute(frame_gray, None)
        keypoints_tracked.append(np.array([kp[i].pt for i in range(len(kp))]))

        frame_idx += 1

    # Reiniciem video
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    #retornem keypoints
    return keypoints_tracked, [0, frame_idx]




if __name__ == '__main__':
    video = cv2.VideoCapture("video/8_unstable.avi")
    keypoints, _ = track_keypoints_orb(video, nfeatures= 300,scaleFactor=1.2,nlevels=1,edgeThreshold=31,fastThreshold=20)
    mostrar_punts(video, keypoints)
    video.release()

    print(f"Punts seguits en {len(keypoints)} frames.")
    
