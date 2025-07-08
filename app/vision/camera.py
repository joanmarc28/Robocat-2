import asyncio
import time
import cv2
import numpy as np
import websockets
from picamera2 import Picamera2
import config


class RobotCamera:
    """Unified camera class with streaming and calibration utilities."""

    def __init__(self, width=config.CAMERA_WIDTH, height=config.CAMERA_HEIGHT, fps=config.CAMERA_FPS):
        self.width = width
        self.height = height
        self.fps = fps

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(main={"size": (width, height)}))
        self.picam2.start()
        self._overlay_boxes = []

        self.face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
        #self.face_cascade_alt = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml")
        self.eye_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_eye.xml")
        #self.eye_glasses = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml")
        self.smile_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_smile.xml")
        #self.cars = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_car.xml")
        #self.fullbody = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_fullbody.xml")

    def add_overlay_box(self, box, label=None, color=(0, 255, 0)):
        """Add a bounding box to be drawn on the next streamed frame."""
        self._overlay_boxes.append((box, label, color))

    def _draw_overlays(self, frame):
        for (x1, y1, x2, y2), label, color in self._overlay_boxes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            if label:
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        self._overlay_boxes.clear()

    def capture_frame(self):
        """Capture a single frame from the camera."""
        return self.picam2.capture_array()

    def capture(self):
        """Return a 3-channel frame for CV/ML pipelines."""
        frame = self.capture_frame()
        if frame is not None and len(frame.shape) == 3 and frame.shape[2] == 4:
            # Picamera2 can return RGBA/BGRA frames. Remove the alpha channel.
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        return frame
    def detecte_cars(self, frame):
        """Detect cars in the frame and draw rectangles around them."""
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        cars = self.cars.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Cotxe", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return frame
    
    def detect_fullbody(self, frame):
        """Detect full bodies in the frame and draw rectangles around them."""
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        bodies = self.fullbody.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Cos complet", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        return frame
    
    def detect_faces(self, frame):
        """Draw rectangles around detected faces, eyes and smiles."""
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Cara", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                cv2.putText(roi_color, "Ull", (ex, ey - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.7, 20)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)
                cv2.putText(roi_color, "Somriure", (sx, sy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        return frame

    async def stream_frames(self, server_url=None):
        url = server_url or f"wss://{config.SERVER_IP}/ws/stream/" + config.ROBOT_ID
        while True:
            try:
                async with websockets.connect(url) as websocket:
                    print("📡 Connectat al servidor")
                    while True:
                        frame = self.capture_frame()
                        frame = self.detect_faces(frame)
                        #frame = self.detecte_cars(frame)
                        #frame = self.detect_fullbody(frame)
                        self._draw_overlays(frame)
                        _, jpeg = cv2.imencode(".jpg", frame)
                        await websocket.send(jpeg.tobytes())
                        await asyncio.sleep(1 / self.fps)
            except Exception as e:
                print(f"❌ Connexió perduda: {e}. Reintentant en 5 segons...")
                await asyncio.sleep(5)


    def take_photo(self, path):
        """Save a single frame to ``path``."""
        frame = self.capture_frame()
        cv2.imwrite(path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def record_video(self, path, duration=5):
        """Record a video for ``duration`` seconds and save it to ``path``."""
        writer = cv2.VideoWriter(
            path,
            cv2.VideoWriter_fourcc(*"XVID"),
            self.fps,
            (self.width, self.height),
        )
        end = time.time() + duration
        while time.time() < end:
            frame = self.capture_frame()
            writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            time.sleep(1 / self.fps)
        writer.release()

    def calibrate(self, pattern="app/sensors/calibrate/img{idx}.jpg", images=9, checkerboard=(8, 6)):
        """Calibrate the camera using chessboard images."""
        obj3DPoints = np.zeros((checkerboard[0] * checkerboard[1], 3), np.float32)
        obj3DPoints[:, :2] = np.mgrid[0 : checkerboard[0], 0 : checkerboard[1]].T.reshape(-1, 2)

        objPoints = []
        imgPoints = []
        img_shape = None

        for idx in range(1, images + 1):
            filepath = pattern.format(idx=idx)
            print(f"Cargando {filepath}")
            im = cv2.imread(filepath)
            if im is None:
                print(f"No s'ha pogut carregar la imatge {filepath}!")
                continue

            im_bw = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            img_shape = im_bw.shape[::-1]
            ret, corners = cv2.findChessboardCorners(im_bw, checkerboard, None)

            if ret:
                objPoints.append(obj3DPoints)
                corners_improved = cv2.cornerSubPix(
                    im_bw, corners, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                )
                imgPoints.append(corners_improved)
                cv2.drawChessboardCorners(im, checkerboard, corners_improved, ret)
                cv2.imshow("calibracio_img", im)
                cv2.waitKey(200)
            else:
                print(f"No s'han trobat cantonades a {filepath}")

        cv2.destroyAllWindows()

        if objPoints and imgPoints and img_shape is not None:
            ret, camera_matrix, distorsion, rot, trans = cv2.calibrateCamera(
                objPoints, imgPoints, img_shape, None, None
            )
            file = cv2.FileStorage("app/sensors/calibrate/camera_calibration.yaml", cv2.FILE_STORAGE_WRITE)
            file.write("camera_matrix", camera_matrix)
            file.write("distorsion_coef", distorsion)
            file.release()
            print("S'han guardat les configuracions a camera_calibration.yaml")
            return camera_matrix, distorsion
        print("No s'ha pogut calibrar la càmera")
        return None, None