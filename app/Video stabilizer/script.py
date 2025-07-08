
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils.visualize import *
from utils.lk_tracker import *
from utils.orb_tracker import *
from utils.sift_tracker import *
from utils.homografia import *
from utils.evaluate import *
from utils.show_keypoints import *
from utils.evaluate import avaluar_estabilitzacio

def show_video_frames_with_keypoints(video_np, keypoints_np, frame_indices=[0, 10, 20, 30]):
    """
    Muestra 4 frames seleccionados del video con sus keypoints.
    - video_np: np.ndarray de shape (frames, height, width, 3)
    - keypoints_np: np.ndarray de shape (frames, n_keypoints, 2)
    - frame_indices: lista con 4 índices de frame a mostrar
    """
    assert len(frame_indices) == 4, "Debes proporcionar 4 índices de frames."

    plt.figure(figsize=(12, 6))

    for i, idx in enumerate(frame_indices):
        frame = video_np[idx].copy()
        kps = keypoints_np[idx]  # (40, 2)

        # Dibujar keypoints
        for (x, y) in kps:
            cv2.circle(frame, (int(x), int(y)), radius=2, color=(0, 255, 0), thickness=-1)

        # Convertir BGR a RGB para matplotlib

        plt.subplot(1, 4, i + 1)
        plt.imshow(frame)
        plt.title(f"Frame {idx}")
        plt.axis("off")

    plt.tight_layout()
    plt.show()

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

def eval(video_aligned, keypoints_np, video_np):
    # Tornem a calcular els keypoints sobre el vídeo estabilitzat
    video_estabilitzat_BGR = np.array([cv2.cvtColor(f, cv2.COLOR_RGB2BGR) for f in video_aligned])
    video_tmp = cv2.VideoWriter("videos/tmp_estabilitzat.avi", cv2.VideoWriter_fourcc(*'XVID'), 30, (video_aligned.shape[2], video_aligned.shape[1]))

    for frame in video_estabilitzat_BGR:
        video_tmp.write(frame)
    video_tmp.release()

    # Obrim el vídeo des de fitxer per passar-lo al tracker
    video_stab_cap = cv2.VideoCapture("videos/tmp_estabilitzat.avi")
    keypoints_stab, _ = track_keypoints_lk(video_stab_cap)
    #keypoints_stab, _ = track_keypoints_orb(video_stab_cap, nfeatures=300,scaleFactor=1.2,nlevels=1,edgeThreshold=31,fastThreshold=20)
    #keypoints_stab, _ = track_keypoints_sift(video_stab_cap)

    video_stab_cap.release()

    # Convertim els keypoints estabilitzats a np.ndarray
    lens_stab = [len(kp) for kp in keypoints_stab]
    max_len_stab = np.min(lens_stab)
    keypoints_stab_np = np.zeros((len(keypoints_stab), max_len_stab, 2))
    for i in range(len(keypoints_stab)):
        for j in range(max_len_stab):
            keypoints_stab_np[i, j, :] = keypoints_stab[i][j]

    #Avaluació de resultats
    avaluar_estabilitzacio(video_np, video_aligned, keypoints_np, keypoints_stab_np)


TRANSFORMATION_MODE = ["translation", "translation+rotation","translation+scale", "affine"]
TRACKING_MODE = ["lk","orb","sift"]

if __name__ == '__main__':
    video = cv2.VideoCapture("videos/unstable/21.avi")
    video_np = load_video_as_numpy("videos/unstable/21.avi")

    Exp = [True,True,True,True]
    # Exp 1
    if Exp[0]:
        t1 = time.time()
        keypoints1, _ = track_keypoints_orb(video)
        t1 = time.time() - t1

        t2 = time.time()
        keypoints2, _ = track_keypoints_sift(video)
        t2 = time.time() - t2

        t3 = time.time()
        keypoints3, _ = track_keypoints_lk(video)
        t3 = time.time() - t3

        print("temps: {:0.04f}s".format(t1))
        mostrar_punts(video, keypoints1, f1=0,f2=40)
        print("temps: {:0.04f}s".format(t2))
        mostrar_punts(video, keypoints2, f1=0,f2=40)
        print("temps: {:0.04f}s".format(t3))
        mostrar_punts(video, keypoints3, f1=0,f2=40)

    # Exp 2
    if Exp[1]:
        vd = video_np[:100]

        t1 = time.time()
        keypoints1, kf = track_keypoints_lk(video, max_corners=1000, min_distance=10)
        kp1 = equal_number_kp(keypoints1)[:100]
        video_aligned1 = align_video(vd, kp1, key_frames=kf, mode="translation")
        t1 = time.time() - t1

        t2 = time.time()
        keypoints2, kf = track_keypoints_lk(video, max_corners=1000, min_distance=20)
        kp2 = equal_number_kp(keypoints2)[:100]
        video_aligned2 = align_video(vd, kp2, key_frames=kf, mode="translation")
        t2 = time.time() - t2

        t3 = time.time()
        keypoints3, kf = track_keypoints_lk(video, max_corners=1000, min_distance=30)
        kp3 = equal_number_kp(keypoints3)[:100]
        video_aligned3 = align_video(vd, kp3, key_frames=kf, mode="translation")
        t3 = time.time() - t3


        print("min_distance=10")
        print("temps: {:0.04f}s".format(t1))
        eval(video_aligned1, kp1, vd)
        mostrar_punts(video, keypoints1, f1=0,f2=40)
        
        print("min_distance=20")
        print("temps: {:0.04f}s".format(t2))
        eval(video_aligned2, kp2, vd)
        mostrar_punts(video, keypoints2, f1=0,f2=40)
        
        print("min_distance=30")
        print("temps: {:0.04f}s".format(t3))
        eval(video_aligned3, kp3, vd)
        mostrar_punts(video, keypoints3, f1=0,f2=40)
        
    #Exp 3
    if Exp[2]:
        vd = video_np[:100]

        keypoints, kf = track_keypoints_lk(video, max_corners=8, min_distance=50)
        kp = equal_number_kp(keypoints)[:100]

        t1 = time.time()
        video_aligned1 = align_video(vd, kp, key_frames=kf, mode=TRANSFORMATION_MODE[0])
        t1 = time.time() - t1

        t2 = time.time()
        video_aligned2 = align_video(vd, kp, key_frames=kf, mode=TRANSFORMATION_MODE[1])
        t2 = time.time() - t2

        t3 = time.time()
        video_aligned3 = align_video(vd, kp, key_frames=kf, mode=TRANSFORMATION_MODE[2])
        t3 = time.time() - t3

        t4 = time.time()
        video_aligned4 = align_video(vd, kp, key_frames=kf, mode=TRANSFORMATION_MODE[3])
        t4 = time.time() - t4

        show_frame(vd, frame=0)
        show_frame(vd, frame=40)

        print(TRANSFORMATION_MODE[0])
        print("temps: {:0.04f}s".format(t1))
        eval(video_aligned1, kp, vd)
        show_frame(video_aligned1)
        
        print(TRANSFORMATION_MODE[1])
        print("temps: {:0.04f}s".format(t2))
        eval(video_aligned2, kp, vd)
        show_frame(video_aligned2)
        
        print(TRANSFORMATION_MODE[2])
        print("temps: {:0.04f}s".format(t3))
        eval(video_aligned3, kp, vd)
        show_frame(video_aligned3)

        print(TRANSFORMATION_MODE[3])
        print("temps: {:0.04f}s".format(t4))
        eval(video_aligned4, kp, vd)
        show_frame(video_aligned4)

    #Exp 4
    if Exp[3]:
        t = time.time()
        vd = video_np
        keypoints, kf = track_keypoints_lk(video, max_corners=8, min_distance=10)
        kp = equal_number_kp(keypoints)
        video_aligned = align_video(vd, kp, key_frames=kf, mode=TRANSFORMATION_MODE[0])
        t = time.time() - t
        
        print("temps: {:0.04f}s".format(t))
        eval(video_aligned, kp, vd)
        mostrar_punts(video, keypoints, f1=0,f2=40)
        
        video_comparation(vd, video_aligned)
    

    video.release()


