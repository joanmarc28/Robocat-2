import cv2
import numpy as np
import matplotlib.pyplot as plt
import time


def video_comparation(video1, video2):
    for f1, f2 in zip(video1, video2):
        # Redimensionar si es necesario para que tengan el mismo tamaño

        shape = (f1.shape[1]//2, f1.shape[0]//2)
        f1 = cv2.resize(f1, shape)[...,::-1]
        f2 = cv2.resize(f2, shape)[...,::-1]

        #f1 = f1[-150+shape[0]//2:150+shape[0]//2, -150+shape[1]//2:150+shape[1]//2]
        #f2 = f2[-150+shape[0]//2:150+shape[0]//2, -150+shape[1]//2:150+shape[1]//2]
        
        # Comparación lado a lado
        comparison = np.hstack((f1, f2))

        cv2.imshow('Original (izquierda) vs Estabilizado (derecha)', comparison)
        
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def show_frame(video, frame=40):

    f = video[frame][...,::-1]

    cv2.imshow('Frame', f)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
