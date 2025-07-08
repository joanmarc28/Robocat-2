from vision.camera import RobotCamera
from ultralytics import YOLO
import os
import pickle
import cv2
import numpy as np
import logging
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
#from tensorflow.keras.models import Sequential, load_model
from keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

PATH = "/home/Robocat/Robocat"
logger = logging.getLogger(__name__)

class PlateDetection:
    #funcions de train (nomes s'executen un cop per crear models yolo i cnn)
    def car_train():
        model = YOLO(PATH+"/app/assets/models/yolov8n.pt")
        results = model.train(
            data=PATH+"/app/assets/yolo/car_model/config_car.yaml",
            epochs=15,          
            imgsz=416,          
            batch=8,            
            device="cpu",  #0 -> gpu, "cpu" -> cpu
            cache=True,         
            workers=4,          
            project=PATH+"/app/assets/yolo/car_model/runs/train_fast",
            name="yolov8n_cotxes"
        )
        return results

    def plate_train():
        model = YOLO(PATH+"/app/assets/models/yolov8n.pt")
        results = model.train(
            data=PATH+"/app/assets/yolo/plate_model/config_plate.yaml",
            epochs=15,          
            imgsz=416,          
            batch=8,            
            device="cpu",  # 0 -> gpu, "cpu" -> cpu
            cache=True,         
            workers=4,          
            project=PATH+"/app/assets/yolo/plate_model/runs/train_fast",
            name="yolov8n_plates"
        )
        return results

    def ocr_train():
        dataset_path = PATH+"/app/assets/database/plate_ocr/chars74k/"
        images = []
        labels = []

        for class_name in os.listdir(dataset_path):
            class_dir = os.path.join(dataset_path, class_name)
            if not os.path.isdir(class_dir):
                continue
            print(f"Llegint classe: {class_name}")
            for img_name in os.listdir(class_dir):
                img_path = os.path.join(class_dir, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                img = cv2.resize(img, (32, 32))
                images.append(img)
                labels.append(class_name)

        print(f"Total imatges carregades: {len(images)}")
        print(f"Total labels carregades: {len(labels)}")

        images = np.array(images) / 255.0
        images = images.reshape(-1, 32, 32, 1)

        label_encoder = LabelEncoder()
        labels_encoded = label_encoder.fit_transform(labels)
        labels_categorical = to_categorical(labels_encoded)

        with open(PATH+"/app/assets/models/label_encoder/label_encoder.pkl", "wb") as f:
            pickle.dump(label_encoder, f)

        X_train, X_test, y_train, y_test = train_test_split(images, labels_categorical, test_size=0.2, random_state=42)

        datagen = ImageDataGenerator(
            rotation_range=5,
            width_shift_range=0.05,
            height_shift_range=0.05,
            zoom_range=0.1,
            shear_range=2,
            fill_mode='nearest'
        )

        cnn = Sequential([
            Conv2D(64, (3,3), activation='relu', input_shape=(32,32,1)),
            MaxPooling2D((2,2)),
            Conv2D(128, (3,3), activation='relu'),
            MaxPooling2D((2,2)),
            Flatten(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(len(label_encoder.classes_), activation='softmax')
        ])

        cnn.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

        print("Training...")
        cnn.fit(datagen.flow(X_train, y_train, batch_size=16),
                epochs=20,
                validation_data=(X_test, y_test))

        #cnn.save(PATH+"/app/assets/models/cnn_plate.h5")
        cnn.save(PATH+"/app/assets/models/cnn_plate.keras", save_format="keras")

    #funcions de deteccio
    def detect_car(frame, camera=None):
        """Detect a car in ``frame``. If ``camera`` is provided, draw the
        detected box on the next streamed frame."""
        logger.info("Detectant cotxe...")
        model = YOLO(PATH+"/app/assets/yolo/car_model/runs/train_fast/yolov8n_cotxes/weights/best.pt")
        results = model.predict(frame, save=True, imgsz=416)  # 0 -> gpu, "cpu" -> cpu
        if results:
            for result in results:
                if result.boxes:
                    logger.info("Cotxe detectat")
                    box = result.boxes[0]
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    if camera is not None:
                        camera.add_overlay_box((x1, y1, x2, y2), label="car")
                    car = frame[y1:y2, x1:x2]
                    return car, (x1, y1, x2, y2)
        logger.info("No s'ha detectat cap cotxe")
        return None, None

    def detect_plate(car, car_bbox=None, camera=None):
        """Detect a licence plate inside ``car`` image. ``car_bbox`` should be
        the bounding box of the car relative to the original frame so the plate
        box can be drawn correctly."""
        model = YOLO(PATH+"/app/assets/yolo/plate_model/runs/train_fast/yolov8n_plates4/weights/best.pt")
        results = model.predict(car, save=True, imgsz=416)
        if results:
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    px1, py1, px2, py2 = map(int, box.xyxy[0].tolist())
                    if camera is not None and car_bbox is not None:
                        cx1, cy1, _, _ = car_bbox
                        camera.add_overlay_box((cx1 + px1, cy1 + py1, cx1 + px2, cy1 + py2), label="plate", color=(0, 0, 255))
                    plate = car[py1:py2, px1:px2]
                    if plate is not None:
                        logger.info("Matrícula detectada")
                        only_plate = PlateDetection.crop_nationality(plate)
                        return only_plate, (px1, py1, px2, py2)
                    else:
                        logger.warning("No s'ha pogut retallar la matrícula")
                        return None, None
        return None, None

    def detect_ocr(plate):
        logger.info("Llegint text de la matrícula...")
        result, char_imgs, chars = PlateDetection.predict_plate_text(plate) #model i label encoder no es toquen!
        logger.info(f"Matrícula reconeguda: {result}")
        return result, char_imgs, chars

    #funcions d'ajuda
    def crop(result, image):
        if result and result[0].boxes and len(result[0].boxes) > 0:
            box = result[0].boxes[0]
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cropped_img = image[y1:y2, x1:x2]
            return cropped_img
        else:
            logger.warning("No s'han trobat cap box a la detecció")
            return None

    
    def preprocess(img): #resize a 32x32 i normalitzacio
        img = cv2.resize(img, (32, 32))
        img = img / 255.0
        return img.reshape(1, 32, 32, 1)
    
    def predict_char(img, model, label_encoder): #funcio predict a partir del model cnn
        x = PlateDetection.preprocess(img)
        pred = model.predict(x)
        label_idx = np.argmax(pred)
        return label_encoder.inverse_transform([label_idx])[0]
    
    def resize_img(img, size=32): #funcio per resize caracters segmentats sense deformar el ratio
        h, w = img.shape
        scale = size / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(img, (new_w, new_h))

        canvas = np.zeros((size, size), dtype=np.uint8) * 255 #fons negre
        x_offset = (size - new_w) // 2
        y_offset = (size - new_h) // 2
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        return canvas
    
    def segment_characters(plate_img):
        logger.info("Segmentant caràcters de la matrícula")
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thr = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        char_regions = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 15 < h < 100 and 5 < w < 80 and h > w:
                char_regions.append((x, y, w, h))

        char_regions = sorted(char_regions, key=lambda b: b[0]) #regions ordenades esq-dreta
        
        char_imgs = []
        for x, y, w, h in char_regions:
            char = thr[y:y+h, x:x+w]
            char = PlateDetection.resize_img(char)
            char = 255 - char #invertir (sino capta el fons com a contorn)
            char_imgs.append(char)
        
        return char_imgs
    
    def predict_plate_text(plate_img, model_path=PATH+"/app/assets/models/cnn.keras", label_encoder_path=PATH+"/app/assets/models/label_encoder/label_encoder.pkl"):
        logger.info("Processant imatge de matrícula per OCR")
        char_imgs = PlateDetection.segment_characters(plate_img)
        text = "" #per guardar el text de la matricula
        #model = load_model(model_path)
        model = load_model(model_path, compile=False, safe_mode=False)
        with open(label_encoder_path, "rb") as f:
            label_encoder = pickle.load(f)
        for char_img in char_imgs:
            processed = PlateDetection.preprocess(char_img)
            prediction = model.predict(processed)
            predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])[0]
            text += predicted_label #afegim la prediccio a text

        corrected = PlateDetection.correct_plate_format(text) #correccio de la matricula (si cal)
        logger.info(f"Text processat: {corrected}")
        return corrected, char_imgs, list(corrected)

    def correct_plate_format(text): #format 1234 BCD
        if len(text) != 7:
            return "No trobada"
        corrected = ""

        #corregeix els numeros (1-4) -> 4 digits
        for i in range(4):
            if text[i].isalpha() and text[i].upper() in ['L', 'S', 'G', 'B']:  # letras que confunden
                if text[i].upper() == 'L':
                    corrected += '4'
                elif text[i].upper() == 'S':
                    corrected += '5'
                elif text[i].upper() == 'G':
                    corrected += '6'
                elif text[i].upper() == 'B':
                    corrected += '8'
            else:
                corrected += text[i]

        #corregeix els caracters (4-7) -> 3 lletres
        for i in range(3):
            if text[i+4].isdigit() and text[i+4] in ['4', '5', '6', '8']: #a partir del index 4
                map_num_to_letter = {'4': 'L', '5': 'S', '6': 'G', '8': 'B'}
                corrected += map_num_to_letter.get(text[i+4], 'A')
            else:
                corrected += text[i+4].upper()

        return corrected

    def crop_nationality(img):
        logger.info("Retallant part de nacionalitat si es detecta blau")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #per detectar el to que ens interessa (blau)
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([130, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_pixels = cv2.countNonZero(mask)

        h, w, _ = img.shape
        blue_ratio = blue_pixels / (h * int(w * 0.15)) #el que s'hauria de tallar si es troba blau (~15% del total de la matricula)

        if blue_ratio > 0.05: #si hi ha algo de blau
            plate_w = int(w * 0.12)
            logger.info("Retallada la banda blava de la matrícula")
            return img[:, plate_w:]
        else:
            logger.info("No s'ha trobat banda blava a la matrícula")
            return img

    

