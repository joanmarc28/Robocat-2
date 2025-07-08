import cv2
import numpy as np
import time

#from show_keypoints import *

#LUCAS - KANADE KEYPOINTS TRACKING

def track_keypoints_lk(video, max_corners=300, quality_level=0.1, min_distance=20, redetect_thresh=0.6):
    key_frames = [0]

    # Mirar si esta obert
    assert video.isOpened(), "Error: no s'ha pogut obrir el vídeo."
    
    # Mirar si te frames
    ret, old_frame = video.read()
    assert ret, "Error: no s'ha pogut obrir el vídeo."



    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_RGB2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, maxCorners=max_corners,
                                 qualityLevel=quality_level,
                                 minDistance=min_distance,
                                 blockSize=3)

    if p0 is None:
        print("Cap punt d'interès detectat.")
        return []
    points_count = len(p0)

    print(points_count)
    

    keypoints_tracked = [p0.reshape(-1, 2)]
    lk_params = dict(winSize=(21, 21), maxLevel=3,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

    frame_idx = 1
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    while frame_idx <= frame_count:
        ret, frame = video.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)




        # Fer tracking dels punts actuals
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        if p1 is None:
            print("Tots els punts s'han perdut.")
            break

        good_new = p1[st == 1].reshape(-1, 2)
        good_old = p0[st == 1].reshape(-1, 2)

        # Comprovar si s'han perdut masses punts
        if len(good_new) < redetect_thresh * points_count:
            key_frames.append(frame_idx)
            print(f"Re-detectant punts al frame {frame_idx} perquè només queden {len(good_new)} punts.")
            p0 = cv2.goodFeaturesToTrack(frame_gray, maxCorners=max_corners,
                                         qualityLevel=quality_level,
                                         minDistance=min_distance,
                                         blockSize=3)
            if p0 is None:
                print("Cap punt d'interès detectat durant re-detecció.")
                break
            points_count = len(p0)
            good_new = p0.reshape(-1, 2)

        keypoints_tracked.append(good_new)

        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)



        frame_idx += 1

    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    key_frames.append(frame_idx)
    return keypoints_tracked, key_frames



if __name__ == '__main__':
    video = cv2.VideoCapture("video/21_unstable.avi")
    keypoints, time_kp = track_keypoints_lk(video,max_corners=300,quality_level=0.1,min_distance=50)
    print("Tracking time spent: ",time_kp)
    mostrar_punts(video, keypoints)
    video.release()

    print(f"Punts seguits en {len(keypoints)} frames.")
