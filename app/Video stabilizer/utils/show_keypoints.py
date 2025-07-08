import cv2
import numpy as np


def mostrar_punts(video, keypoints_tracked, f1=0, f2=40):
    """
    - f1, f2: índexs dels fotogrames a visualitzar
    """

    if not video.isOpened():
        print("⚠️ Error: no s'ha pogut obrir el vídeo.")
        return

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if f1 >= total_frames or f2 >= total_frames:
        print(f"⚠️ Els fotogrames f1={f1} o f2={f2} excedeixen la durada del vídeo ({total_frames} fotogrames).")
        return

    # Llegim els fotogrames
    video.set(cv2.CAP_PROP_POS_FRAMES, f1)
    ret1, frame1 = video.read()

    video.set(cv2.CAP_PROP_POS_FRAMES, f2)
    ret2, frame2 = video.read()

    if not (ret1 and ret2):
        print(f"⚠️ No s'han pogut llegir els fotogrames {f1} i {f2}.")
        return

    # Dibuixa punts al frame f1
    if f1 < len(keypoints_tracked):
        for pt in keypoints_tracked[f1]:
            x, y = int(pt[0]), int(pt[1])
            cv2.circle(frame1, (x, y), 4, (0, 255, 0), -1)
    else:
        print(f"⚠️ No hi ha punts disponibles pel frame {f1}.")

    # Dibuixa punts al frame f2
    if f2 < len(keypoints_tracked):
        for pt in keypoints_tracked[f2]:
            x, y = int(pt[0]), int(pt[1])
            cv2.circle(frame2, (x, y), 4, (0, 255, 0), -1)
    else:
        print(f"⚠️ No hi ha punts disponibles pel frame {f2}.")

    # Combina i mostra les imatges
    combinada = np.concatenate((frame1, frame2), axis=1)
    cv2.imshow(f"Punts en frame {f1} (esquerra) i {f2} (dreta)", combinada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
