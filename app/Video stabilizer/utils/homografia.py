import cv2
import matplotlib.pyplot as plt
import numpy as np

"""
def align_images(current_frame, prev_keypoints, current_keypoints):
    pk = prev_keypoints
    ck = current_keypoints
    if prev_keypoints.shape[0] > current_keypoints.shape[0]:
        pk = prev_keypoints[:current_keypoints.shape[0]]
    elif prev_keypoints.shape[0] < current_keypoints.shape[0]:
        ck = current_keypoints[:prev_keypoints.shape[0]]

    H, mask = cv2.estimateAffinePartial2D(ck, pk, cv2.RANSAC, ransacReprojThreshold=3.0)

    aligned_source = cv2.warpAffine(current_frame, H, (current_frame.shape[1], current_frame.shape[0]))

    return aligned_source, mask"""

def align_images(current_frame, prev_keypoints, current_keypoints, mode="translation"):
    pk = prev_keypoints
    ck = current_keypoints
    if pk.shape[0] > ck.shape[0]:
        pk = pk[:ck.shape[0]]
    elif ck.shape[0] > pk.shape[0]:
        ck = ck[:pk.shape[0]]

    if mode == "translation":
        translation = np.mean(pk - ck, axis=0)
        H = np.array([
            [1, 0, translation[0]],
            [0, 1, translation[1]]
        ], dtype=np.float32)
        aligned = cv2.warpAffine(current_frame, H, (current_frame.shape[1], current_frame.shape[0]))
        return aligned, None

    elif mode == "affine":
        H, mask = cv2.estimateAffinePartial2D(ck, pk, cv2.RANSAC, ransacReprojThreshold=3.0)
        aligned = cv2.warpAffine(current_frame, H, (current_frame.shape[1], current_frame.shape[0]))
        return aligned, mask

    elif mode == "translation+rotation":
        # Center keypoints
        pk_centered = pk - np.mean(pk, axis=0)
        ck_centered = ck - np.mean(ck, axis=0)

        # Estimate rotation using SVD
        U, _, VT = np.linalg.svd(ck_centered.T @ pk_centered)
        R = U @ VT
        angle = np.arctan2(R[1, 0], R[0, 0])

        # Compute translation after rotation
        center_ck = np.mean(ck, axis=0)
        center_pk = np.mean(pk, axis=0)

        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        H = np.array([
            [cos_a, -sin_a, center_pk[0] - (cos_a * center_ck[0] - sin_a * center_ck[1])],
            [sin_a,  cos_a, center_pk[1] - (sin_a * center_ck[0] + cos_a * center_ck[1])]
        ], dtype=np.float32)

        aligned = cv2.warpAffine(current_frame, H, (current_frame.shape[1], current_frame.shape[0]))
        return aligned, None

    elif mode == "translation+scale":
        # Compute scales and translation
        scale = np.linalg.norm(pk[1] - pk[0]) / np.linalg.norm(ck[1] - ck[0])
        translation = np.mean(pk - ck * scale, axis=0)

        H = np.array([
            [scale, 0, translation[0]],
            [0, scale, translation[1]]
        ], dtype=np.float32)

        aligned = cv2.warpAffine(current_frame, H, (current_frame.shape[1], current_frame.shape[0]))
        return aligned, None

    else:
        raise ValueError("Mode no reconegut. Usa 'translation', 'affine', 'translation+rotation' o 'translation+scale'.")



"""
def align_video(video, key_points):
    video_aligned = np.zeros(video.shape).astype(np.uint8)
    video_aligned[0] = video[0]
    for i in range(1, 200):
        video_aligned[i], _ = align_images(video[i], key_points[0], key_points[i])
    return video_aligned

if __name__ == '__main__':
    frame = np.zeros((100,100,3)).astype(np.uint8)

    video = np.stack((frame,frame,frame),axis=0)

    video[0, 10:60, 10:60, 0] = 255
    video[1, 20:70, 20:70, 0] = 255
    video[2, 20:70, 30:80, 0] = 255

    key_points = np.zeros((3,4,2))

    key_points[0,0,:] = [10,10]
    key_points[0,1,:] = [10,60]
    key_points[0,2,:] = [60,10]
    key_points[0,3,:] = [60,60]

    key_points[1,0,:] = [20,20]
    key_points[1,1,:] = [20,70]
    key_points[1,2,:] = [70,20]
    key_points[1,3,:] = [70,70]

    key_points[2,0,:] = [30,20]
    key_points[2,1,:] = [30,70]
    key_points[2,2,:] = [80,20]
    key_points[2,3,:] = [80,70]

    video_aligned = align_video(video, key_points)

    video[0,:,:,1] = video[0,:,:,0]
    video[1,:,:,1] = video[0,:,:,0]
    video[2,:,:,1] = video[0,:,:,0]

    video_aligned[0,:,:,1] = video[0,:,:,0]
    video_aligned[1,:,:,1] = video[0,:,:,0]
    video_aligned[2,:,:,1] = video[0,:,:,0]

    fig, ax = plt.subplots(nrows=3,ncols=2)
    print(video_aligned.shape)
    for i in range(3):
        ax[i,0].imshow(video[i])
        ax[i,0].plot(*np.transpose(key_points[i]),'o')
        ax[i,0].set_axis_off()

        ax[i,1].imshow(video_aligned[i])
        ax[i,1].set_axis_off()
    plt.show()"""

def align_video(video, key_points, key_frames=[0], mode="translation"):
    video_aligned = np.zeros_like(video).astype(np.uint8)

    video_aligned[0] = video[0]
    current_kf = 0
    for i in range(1, len(video)):
        if len(key_frames) != current_kf+1 and i == key_frames[current_kf+1]: current_kf += 1
        print(i,current_kf)
        aligned_frame, _ = align_images(video[i], key_points[key_frames[current_kf]], key_points[i], mode=mode)
        video_aligned[i] = aligned_frame
    return video_aligned
