import cv2
import numpy as np

def track_keypoints(video, max_corners=300, quality_level=0.1, min_distance=10):
    if not video.isOpened():
        print("Error: no s'ha pogut obrir el vídeo.")
        return []

    ret, old_frame = video.read()
    if not ret:
        print("Error: no s'ha pogut llegir el primer fotograma.")
        return []

    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray,
                                 maxCorners=max_corners,
                                 qualityLevel=quality_level,
                                 minDistance=min_distance,
                                 blockSize=3)

    if p0 is None:
        print("Cap punt d'interès detectat.")
        return []

    keypoints_tracked = [p0.reshape(-1, 2)]
    lk_params = dict(winSize=(21, 21), maxLevel=3,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

    frame_idx = 1
    while frame_idx <= 200:  # només seguim fins el frame 40
        ret, frame = video.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        if p1 is None:
            break

        good_new = p1[st == 1].reshape(-1, 2)
        keypoints_tracked.append(good_new)

        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)
        frame_idx += 1

    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return keypoints_tracked


def mostrar_punts_frame0_i_40(video, keypoints_tracked):
    if not video.isOpened():
        print("Error: no s'ha pogut obrir el vídeo.")
        return

    # Llegim frame 0 i frame 40
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame0 = video.read()
    video.set(cv2.CAP_PROP_POS_FRAMES, 40)
    ret2, frame40 = video.read()

    if not (ret and ret2):
        print("No s'han pogut llegir els fotogrames 0 i 40.")
        return

    # Dibuixem els punts d'interès
    for pt in keypoints_tracked[0]:
        x, y = pt
        cv2.circle(frame0, (int(x), int(y)), 4, (0, 255, 0), -1)

    if len(keypoints_tracked) > 40:
        for pt in keypoints_tracked[40]:
            x, y = pt
            cv2.circle(frame40, (int(x), int(y)), 4, (0, 255, 0), -1)

    imatges = np.concatenate((frame0, frame40), axis=1)
    cv2.imshow("Frame 0 (esquerra) i Frame 40 (dreta)", imatges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video = cv2.VideoCapture("video/21_stable.avi")
    keypoints = track_keypoints(video)
    mostrar_punts_frame0_i_40(video, keypoints)
    video.release()

    print(f"Punts seguits en {len(keypoints)} frames.")
