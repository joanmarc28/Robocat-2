import numpy as np
import cv2

def calcular_moviment_residual(keypoints_np):
    """
    Calcula la distància mitjana i desviació dels punts entre frames consecutius.
    """
    distancies = []
    for i in range(1, keypoints_np.shape[0]):
        prev = keypoints_np[i - 1]
        curr = keypoints_np[i]

        # Evita problemes si hi ha diferències en la longitud
        n = min(len(prev), len(curr))
        dists = np.linalg.norm(curr[:n] - prev[:n], axis=1)
        distancies.append(np.mean(dists))

    return np.mean(distancies), np.std(distancies)

def calcular_nitidesa(video_np):
    """
    Retorna la mitjana de nitidesa d'un vídeo (usant variància Laplaciana).
    """
    valors = []
    for frame in video_np:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        valors.append(lap.var())
    return np.mean(valors)

def avaluar_estabilitzacio(video_original_np, video_estabilitzat_np, keypoints_original_np, keypoints_estabilitzat_np):
    """
    Avalua el grau d'estabilització aplicat sobre un vídeo.
    """

    print("Calculant moviment residual original...")
    mov_mitja_before, mov_std_before = calcular_moviment_residual(keypoints_original_np)

    print("Calculant moviment residual després d'estabilitzar...")
    mov_mitja_after, mov_std_after = calcular_moviment_residual(keypoints_estabilitzat_np)

    print("Calculant nitidesa...")
    sharp_before = calcular_nitidesa(video_original_np)
    sharp_after = calcular_nitidesa(video_estabilitzat_np)

    print("\n📊 Resultats de l'avaluació:")
    print(f"Moviment abans:     Mitjana = {mov_mitja_before:.2f},  Desviació = {mov_std_before:.2f}")
    print(f"Moviment després:  Mitjana = {mov_mitja_after:.2f},  Desviació = {mov_std_after:.2f}")
    print(f"Nitidesa abans: {sharp_before:.2f}")
    print(f"Nitidesa després: {sharp_after:.2f}")

