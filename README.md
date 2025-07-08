<h1 align="center">
  <br>
    <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/RoboCat_Logo.svg" alt="RoboCat Logo" width="250">
  <br>
    RoboCat
  <br>
</h1>

<h4 align="center">A quadruped robot developed by third-year Computer Science students at the Universitat Autònoma de Barcelona.</h4>

<p align="center">
  <!----------------------- UAB | Robótica ----------------------->
  <a href="https://rlpengineeringschooluab.wordpress.com"><img src="https://img.shields.io/badge/UAB-RLP-3FB911" alt="UAB | RLP"></a>
  <!--------------------------- Status --------------------------->
  <img src="https://img.shields.io/badge/status-prototype-4CB696" alt="Status | Prototype">
  <!---------------------------  Raspi --------------------------->
  <a href="https://www.raspberrypi.com/">
  <img src="https://img.shields.io/badge/-Raspberry%20Pi-A22846?logo=Raspberry%20Pi&logoColor=white" alt="Raspberry Pi Badge"></a>
  <!--------------------------- THX U ---------------------------->
  <img alt="Thank You <3!" src="https://img.shields.io/badge/%3C3-Thank_you!-blue">
  
</p>

 <!---Modificar per els nostres casos--->
<p align="center">
  <a href="#What-is-RoboCat">What is RoboCat?</a> •
  <a href="#How-To-Use">How to use</a> •
  <a href="#Components">Components</a> •
  <a href="#Software">Software</a> •
  <a href="#Tech-Stack">Tech Stack</a> •
  <a href="#License">License</a> •
  <a href="#Contribution">Contribution</a> •
  <a href="#References">References</a> •
  <a href="#Credits">Credits</a> •
  <a href="#Gallery">Gallery</a>
</p>

![screenshot](https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/model_360.gif)


# What is RoboCat?

RoboCat is an autonomous quadruped robot designed to patrol public streets and monitor parking zones regulated by payment. Its structure and external appearance are inspired by a cat's shape, making it functional but also friendly and approachable for pedestrians.
Equipped with sensors, cameras and onboard computing, RoboCat can detect whether a parked vehicle has an active parking permit, combining robotics, computer vision and real-time data processing to offer a smart, mobile solution for urban mobility enforcement.

The project's main goals are to:
  - Automate parking control in regulated areas
  - Reduce the need for manual inspection
  - Integrate urban robotics with a friendly and non-threatening design
  - Demonstrate the application of robotics in real-world city environments

<p align="center">
  <a href="https://www.youtube.com/watch?v=SMAzvaqW83E" target="_blank">
    <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/app/RoboCat_miniatura.png" alt="Miniatura del vídeo" width="600">
  </a>
</p>
<p>
  <a href="https://www.youtube.com/watch?v=SMAzvaqW83E" target="_blank">
    View Video on YouTube
  </a>
</p>
  
# How to use

To set up and run RoboCat on your system, follow these simple steps:
### Step 1: Download the repository
Open your terminal and run the following command:
```bash
git clone https://github.com/joanmarc28/Robocat.git
cd Robocat
```
### Step 2: Install dependencies
Make sure you have Python installed. You can install the required environment simply by running the file setup_robocat.sh:
```bash
bash setup_robocat.sh
```
You can run this command even if the robot is powered off. The setup process only installs software on your computer.

#### How do I install Python?
If you don't have Python installed, download it from the [official website](https://www.python.org/downloads/)
You can check your Python version by running:
```bash
python --version
```
### Step 3: Activate the environment
Once the installation is complete, activate the virtual environment and run the main program by running the following command:
```bash
bash start_robocat.sh
```
Now you can just enjoy!

# Components

## Hardware 

The RoboCat prototype integrates various electronic modules connected to the Raspberry Pi 4, which is the central processing unit.

### Required components
| Component | Model | Units |
|-----------|-------|-------|
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/raspberrypi4.jpg" width="75"> | [Raspberry Pi 4 Model B](https://tienda.bricogeek.com/placas-raspberry-pi/1330-raspberry-pi-4-model-b-4-gb.html) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/controlador_servos.jpg" width="75"> | [PCA9685 (16 channel PWM controller)](https://tienda.bricogeek.com/controladores-motores/1764-controlador-pwm-16-canales-i2c-pca9685.html) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/servo.jpg" width="75"> | [MG996R Digital Servomotor](https://tienda.bricogeek.com/servomotores/1684-servomotor-digital-mg996r.html?gad_source=1&gclid=CjwKCAjwwLO_BhB2EiwAx2e-3w-vAP7yfwU6gmF38uj6yTVi2fuEX_7WWVGUK1a4Pqmh1sUbJGIflBoC-XYQAvD_BwE) | 9 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/gps.jpg" width="75"> | [GPS BN-880 (Dual GPS/GLONASS with integrated compass)](https://tienda.bricogeek.com/modulos-gps/1638-gps-glonass-dual-bn-880-con-antena.html) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/camera.png" width="75"> | [Camera OV5647 for Raspberry Pi (V2)](https://tienda.bricogeek.com/accesorios-raspberry-pi/822-camara-raspberry-pi-v2-8-megapixels.html) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/ultrasons.jpg" width="75"> | [Ultrasonic Distance Sensor HC-SR04](https://tienda.bricogeek.com/sensores-distancia/741-sensor-de-distancia-por-ultrasonidos-hc-sr04.html) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/accelero-giro.jpg" width="75"> | [GY-521 MODULE (MPU-6050 accelerometer and gyro)](https://tienda.bricogeek.com/acelerometros/1682-modulo-gy-521-acelerometro-y-giroscopio-mpu-6050.html) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/lipo.png" width="75"> | [3500mAh 2S 25C LiPo Battery (7.4V)](https://tienda.bricogeek.com/baterias-lipo/1156-bateria-lipo-3500mah-2s-25c-74v.html) | 2 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/polulu.jpg" width="75"> | [DC-DC 5V 3A - S13V30F5 Voltage Conversor](https://tienda.bricogeek.com/convertidores-de-voltaje/1746-conversor-dc-5v-3a-s13v30f5.html) | 2 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/amplificador.jpg" width="75"> | [FEICHAO 8A UBEC 2-6S LiPo (In 7V-25.5V, Out 12A)](https://www.amazon.es/dp/B07DD9L6P6?ref=ppx_yo2ov_dt_b_fed_asin_title) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/microfon.jpg" width="75"> | [eModwey Microphone Lavalier USB 2M](https://www.amazon.es/dp/B0DNDT5DRQ?ref=ppx_yo2ov_dt_b_fed_asin_title) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/amplificador.jpg" width="75"> | [Audio Amplificator I2S MAX98357 (3W)](https://tienda.bricogeek.com/accesorios-raspberry-pi/867-amplificador-de-audio-i2s-max98357a-3w.html?gad_source=1&gad_campaignid=17337431439&gbraid=0AAAAADkb14fI-X2E-Gh7r06Difb1Wd5aD&gclid=Cj0KCQjwrPHABhCIARIsAFW2XBPmEQGgPAAcVo2H_3N5DqCXDw7oVZT2QkZupvooRj8hKRmd9Y1jEiYaAq5tEALw_wcB) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/altaveu.jpg" width="75"> | [Speaker in Box (Ref: PRO-0162)](https://tienda.bricogeek.com/varios/938-altavoz-con-caja-3w.html?_gl=1*1r6tjg0*_up*MQ..*_gs*MQ..&gclid=Cj0KCQjwrPHABhCIARIsAFW2XBOtxb4ms0BOJzoKjZsUEEGlDNfoNcSNstp5hDVbZeetJuUue8356fEaAuGHEALw_wcB&gbraid=0AAAAADkb14cQMXRSKfpouRgVtJaYG1zOD) | 1 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/oled.png" width="75"> | [OLED Screen Module SSD1306 GME12864-11-12-13 (0.96in, 128x64)](https://goldenmorninglcd.com/es/m%C3%B3dulo-de-pantalla-oled/0.96-pulgadas-128x64-ssd1306-gme12864-11/) | 2 |
| <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/img_components/UBEC.jpg" width="75"> | [FEICHAO 8A UBEC Salida MAX 12A Entrada 7V-25.5V 2-6S Lipo](https://www.amazon.es/dp/B07DD9L6P6?ref=ppx_yo2ov_dt_b_fed_asin_title) | 1 |

### Wiring Schematics
The wiring schematics shown below have been created using Fritzing for clarity during the assembly process.
<div align="center"><img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/Hardware/Esquema%20B.png" width="800"> </div> <br>

> [!NOTE]
> However, a custom PCB has been designed using EasyEDA to ensure a compact assembly for the final RoboCat unit, which can be seen in the following <a href="https://github.com/joanmarc28/Robocat/blob/main/Hardware/PCB%20Robocat%20Disseny.png">link.</a>

## 3D Design

All RoboCat 3D parts have been designed using Autodesk Fusion 360. The structure is divided into the following parts, and the printing parameters for each piece can be found in its corresponding folder.

### Legs
| Full Leg |
|----------|
| <div align="center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/legs/leg_video.gif" width="200"><br>[Leg (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/legs)</div> |


---

### Body

| Chassis | Second Floor Plate |
|---------|--------------------|
| <div align="center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/chassis/chassis_video.gif" width="200"> <br> [Chassis (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/chassis) </div> | <div align="center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/2nFloor_Plate/2nFloor_plate_video.gif" width="200">  <br> [2nd Floor Plate (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/2nFloor_Plate) </div>|

| Front Body | Middle Body | Back Body |
|------------|-------------|-----------|
| <div align ="center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/front_body/front_body_video.gif" width="200"> <br> [Front Body (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/front_body) </div> | <div align="center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/middle_body/middle_body_video.gif" width="200"> <br> [Middle Body (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/middle_body) </div> | <div align="center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/back_body/back_body_video.gif" width="200"> <br> [Back Body (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/back_body) </div> |

---

### Head

| Neck | Head Model | Head Back Panel |
|------|------------|-----------------|
| <div align = "center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/neck/neck_video.gif" width="200"> <br>  [Neck (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/neck) </div> | <div align="center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/head/head_video.gif" width="200"> <br> [Head Model (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/head) </div> | <div align="center">  <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/head/head_back_panel_video.gif" width="200"> <br> [Head Back Panel (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/head) </div> |

---

### Miscellaneous

| Tail | Fan |
|------|-----|
| <div align = "center"> <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/tail/tail_video.gif" width="200"> <br> [Tail (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/tail/tail.stl) </div> | <div align="center">  <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/3D_files/fan/fan_video.gif" width="200"> <br> [Fan (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/fan)</div> |

---

# Software
The RoboCat software is composed of three main components:
- License Plate Detection Algorithm
- Inverse Kinematics for Walking
- Web Application

## License Plate Detection Algorithm
RoboCat integrates a computer vision system that operates in three phases to detect and process license plates:
#### 1. Vehicle Detection
Using YOLOv8n object detection model, RoboCat identifies vehicles present in its field of vision. Specifically, the system is trained to detect only conventional passenger cars, the only object class configured in the YOLO model for this detection task. This selective approach ensures optimized performance and reduces false positives from unrelated objects.

<p align="center">
  <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/car detection.jpeg" alt="Car detection" width="350">  
</p>

#### 2. License Plate Detection
Once a vehicle is detected, a second YOLOv8n model is used to locate the license plate area accurately. The system also detects and extracts the nationality region by identifying the blue section commonly present on Spanish license plates. Since our project only focuses on Spanish license plates, the blue section is cropped for further processing.

<p align="center">
  <img align="middle" src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/license detection.jpeg" alt="plate detection" width="350">&nbsp;&nbsp;&nbsp;&nbsp;<img align="middle" src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/license cut.png" alt="cutted plate" width="250">
</p>

#### 3. Optical Character Recognition (OCR)
For text extraction from license plates, RoboCat uses Gemini AI, a multimodal system capable of performing OCR tasks with high accuracy, eliminating the need for manual character segmentation and traditional CNN-based recognition.
However, the project includes a complete implementation of an OCR system based on a TensorFlow Convolutional Neural Network (CNN), which can serve as a backup or for research purposes. This CNN model performs character segmentation, individual recognition, and post-processing to ensure compliance with the Spanish license plate format (e.g., 1234 BCD), including correction mechanisms to mitigate common character misclassification.

<p align="center">
  <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/matricula.png" alt="Character identification" width="550">  
</p>

## Inverse Kinematics for Walking
<table style="border: none;" >
<tr>
<td width="40%">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/inverse_kinematics_demo.gif" width="100%">
</td>
<td>

RoboCat's locomotion is based on an Inverse Kinematics system, which allows precise control of the robot's legs to perform complex movements such as walking or interacting with its environment. Unlike forward kinematics, where joint angles are known and the resulting position is computed, inverse kinematics solves the opposite problem: determining the necessary joint angles to achieve a desired position or orientation of the legs.

The inverse kinematics models and animations have been designed and tested using CoppeliaSim, a robotics simulation environment, allowing us to prototype and optimize the movements before deployment on the real robot.

Currently, RoboCat supports the following pre-programmed movement modes using inverse kinematics.

</td>
</tr>
</table>


 | Walk | Sit | Playful |
 |------|-----|---------|
 | <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/walk_ani.gif" width="300"> | <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/sit_ani.gif" width="300"> | <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/paw_ani.gif" width="300"> |

## Web Application
The RoboCat system is built on a layered software architecture that separates concerns across user interaction, server-side processing, and robot-level execution. This structured approach enhances modularity, scalability, and maintainability while enabling seamless coordination between autonomous robotic units and central control. The following diagram illustrates the core components and responsibilities distributed across the User, Server, and Robot levels.

<div align="center"><img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/app/diagrama.png" width="800"> </div><br>
As we can see, the web application includes two user profiles.

### Police Officer
Authorized officers can access a control interface to monitor and manage RoboCat units in real-time:
- Live location tracking (GPS coordinates)
- Internal system monitoring, including controller temperature
- Real-time video feed from RoboCat's onboard camera
- Remote control commands such as "Crouch" or "Stand Up"

In addition, officers can manage regulated parking areas through the Parking Zone Management page, where new parking zones can be defined by specifying latitude and longitude boundaries.
Officers also have access to the Infraction Database, where they can review all detected violations, manually validate or dismiss possible infractions, and issue fines when necessary.
<p>
  <a href="https://www.youtube.com/watch?v=kHLnomrDODU" target="_blank">
    <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/web_patrol/RoboCat_PoliceAPP_miniatura.png" alt="Miniatura del vídeo" width="300">
  </a>
</p>
<p>
  <a href="https://www.youtube.com/watch?v=kHLnomrDODU" target="_blank">
    View Video on YouTube
  </a>
</p>

### Client (Vehicle Owner)

Registered users can manage their vehicles and parking sessions through the web platform:
- Register one or more vehicles by providing license plate, brand, model and official DGT data.
- Pay for parking in regulated zones by selecting a registered vehicle and specifying the desired parking duration
- Active parking sessions are displayed on the main dashboard with a countdown timer showing the remaining time.

If a vehicle is parked without a valid registration in a regulated area and RoboCat scans its license plate, an infraction is automatically recorded. The system notifies the vehicle owner of the violation and provides the fine details.

<p>
  <a href="https://www.youtube.com/watch?v=OOTuV0h7_Dc" target="_blank">
    <img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/web_parking/RoboCat_CarPay_miniatura.png" alt="Miniatura del vídeo" width="300">
  </a>
</p>
<p>
  <a href="https://www.youtube.com/watch?v=OOTuV0h7_Dc" target="_blank">
    View Video on YouTube
  </a>
</p>

# Tech Stack
### Programming & AI
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="python"></a>
<a href="https://opencv.org/"><img src="https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"></a>
<a href="https://www.ultralytics.com/"><img src="https://img.shields.io/badge/ultralytics-a061ff.svg?style=for-the-badge&logo=YOLO&logoColor=ffffff&labelColor=a061ff" alt="Ultralytics"></a>
<a href="https://www.tensorflow.org/"><img src="https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white" alt="TensorFlow"></a>
<a href="https://numpy.org/"><img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"></a>
  
### 3D Design & Hardware
<a href="https://www.autodesk.com/"><img src="https://img.shields.io/badge/autodesk-fusion-ff781f.svg?style=for-the-badge&logo=Autodesk&logoColor=ffffff&labelColor=ff781f" alt="Fusion 360"></a>
<a href="https://fritzing.org/"><img src="https://img.shields.io/badge/FRITZING-bf0000.svg?style=for-the-badge&logo=FileZilla&logoColor=ffffff&labelColor=bf0000" alt="Fritzing"></a>
<a href="https://easyeda.com/"><img src="https://img.shields.io/badge/easyeda-2b96da.svg?style=for-the-badge&logo=EDEKA&logoColor=ffffff&labelColor=2b96da" alt="EasyEDA"></a>

### Simulation & Development Tools
<a href="https://www.coppeliarobotics.com/"><img src="https://img.shields.io/badge/coppelia-robotics-c80000.svg?style=for-the-badge&logo=Circle&logoColor=ffffff&labelColor=c80000" alt="CoppeliaSIM"></a>
<a href="https://code.visualstudio.com/"><img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white" alt="VS Code"></a>
<a href="https://pypi.org/project/python-dotenv/"><img src="https://img.shields.io/badge/python-dotenv-3776ab.svg?style=for-the-badge&logo=Python&logoColor=ffffff&labelColor=3776ab" alt="Python DotEnv"></a>

### Web Application
| Backend | Frontend |
|---------|----------|
| <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI"></a> | <a href="https://jinja.palletsprojects.com/en/stable//"><img src="https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black" alt="Jinja"></a> |

| Database | APIs & External Services |
|----------|--------------------------|
| <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"></a> | <a href="https://cloud.google.com/vision"><img src="https://img.shields.io/badge/cloud-vision-4285f4.svg?style=for-the-badge&logo=GoogleCloud&logoColor=ffffff&labelColor=4285f4" alt="CloudVision"></a> <a href="https://cloud.google.com/speech-to-text"><img src="https://img.shields.io/badge/cloud-speech-4285f4.svg?style=for-the-badge&logo=GoogleCloud&logoColor=ffffff&labelColor=4285f4" alt="CloudSpeech"></a> <br> <a href="https://ai.google.dev/?utm_source=website&utm_medium=referral&utm_campaign=geminichat&utm_contentn"><img src="https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white" alt="Google Gemini"></a> <a href="https://github.com/aiortc"><img src="https://img.shields.io/badge/AIORTC-2c5bb4.svg?style=for-the-badge&logo=AIOHTTP&logoColor=ffffff&labelColor=2c5bb4" alt="Aiortc"></a> |
  
# License
This project is licensed under the [MIT License](LICENSE).  
© 2025–present [Contributors](https://github.com/joanmarc28/Robocat/contributors)

# Contribution
This project was created as part of a university assignment and is not open to external contributions.

However, feel free to fork the repository and experiment with it for learning and improvement purposes.

# References
**1** | *Tutorial EasyEDA* ([Link](https://www.youtube.com/watch?v=BvvHJ-H79l8&ab_channel=ELECTRONOOBSenEspa%C3%B1ol)) <br>

**2** | *The LAD Dog V1.0 - Assembly Instructions* ([Link](https://www.youtube.com/watch?v=YNgyFZvyQP4&ab_channel=LADRobotics)) <br>

**3** | *OpenCat by PetoiCamp* ([Link](https://github.com/PetoiCamp/OpenCat)) <br>

**4** | *Boston Dynamics Robot* ([Link](https://www.youtube.com/watch?v=9KdLYhsh0zw&ab_channel=SabinIngenier%C3%ADaCivil)) <br>

**5** | *Beitian BN220 GPS Installation* ([Link](https://www.youtube.com/watch?v=30FU0_7-G3w&ab_channel=Unboxingexperience7)) <br>

**6** | *Sistema de detección de matrículas con OpenCV (Jorge Navacerrada)* ([Link](https://oa.upm.es/51869/1/TFG_JORGE_NAVACERRADA.pdf)) <br>

**7** | *Car License Plate Detection Database* ([Link](https://www.kaggle.com/datasets/andrewmvd/car-plate-detection/data)) <br>

**8** | *Chars74K Database for OCR Training* ([Link](https://www.kaggle.com/datasets/supreethrao/chars74kdigitalenglishfont))

# Credits

<table align="center">
  <tr>
    <td align="center" style="border:none;">
      <img src="https://drive.google.com/uc?export=view&id=182neS8AfRccrTfZxhhOWW1_33He05jec" style="width:120px; height:120px; border-radius:50%; object-fit:cover;" alt="Martí Armengod Villar"/><br/>
      <span style="font-size:14px;"><strong>Martí Armengod Villar</strong></span><br/>
      <span style="font-size:12px;"><em>SW Lead</em></span>
    </td>
    <td align="center" style="border:none;">
      <img src="https://drive.google.com/uc?export=view&id=10n86a7ojWd_smrINd2Kd0ascUYU9XNRo" style="width:120px; height:120px; border-radius:50%; object-fit:cover;" alt="Lara Castillejo Roig"/><br/>
      <span style="font-size:14px;"><strong>Lara Castillejo Roig</strong></span><br/>
      <span style="font-size:12px;"><em>Testing & Validation Lead</em></span>
    </td>
    <td align="center" style="border:none;">
      <img src="https://drive.google.com/uc?export=view&id=1beCsVFoD9ogQ_LeVuKoXPReSoyoeAkFH" style="width:120px; height:120px; border-radius:50%; object-fit:cover;" alt="Julia Lipin Gener Rey"/><br/>
      <span style="font-size:14px;"><strong>Julia Lipin Gener Rey</strong></span><br/>
      <span style="font-size:12px;"><em>3D & Mechanical Lead</em></span>
    </td>
    <td align="center" style="border:none;">
      <img src="https://drive.google.com/uc?export=view&id=1vqmqJ6zK3hYvRlv5AfvEHue0tsL_oQew" style="width:120px; height:120px; border-radius:50%; object-fit:cover;" alt="Joan Marc Samó Rojas"/><br/>
      <span style="font-size:14px;"><strong>Joan Marc Samó Rojas</strong></span><br/>
      <span style="font-size:12px;"><em>Product Owner</em></span>
    </td>
    <td align="center" style="border:none;">
      <img src="https://drive.google.com/uc?export=view&id=16fCYusOWvp_Bf6fR0YFLo8GPbOtSsn5x" style="width:120px; height:120px; border-radius:50%; object-fit:cover;" alt="Luís Vera Albarca"/><br/>
      <span style="font-size:14px;"><strong>Luís Vera Albarca</strong></span><br/>
      <span style="font-size:12px;"><em>HW Lead</em></span>
    </td>
  </tr>
</table>

Special thanks to:
- **Pau Bofill** for collaborating with the license plate detection algorithm and making it possible.
- **Marc Bardeli** for collaborating with the web application implementation.

# Gallery
<p align>
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/walking_uni.gif" alt="RoboCat Logo" width="480"> 
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/spread_legged.jpeg" alt="RoboCat Logo" width="300">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/stretch.jpeg" alt="RoboCat Logo" width="450">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/eyes_head.gif" alt="RoboCat Logo" width="270">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/legs_assembly.jpeg" alt="RoboCat Logo" width="310">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/legs_testing.gif" alt="RoboCat Logo" width="400">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/poser.jpeg" alt="RoboCat Logo" width="400">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/first_body.jpeg" alt="RoboCat Logo" width="400">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/pcb.jpeg" alt="RoboCat Logo" width="370">
<img src="https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/chassis_print.jpeg" alt="RoboCat Logo" width="280">
</p>
