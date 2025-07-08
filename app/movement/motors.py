import math
import time
import config
import board
import busio
import numpy as np
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import threading
from sensors.ultrasonic import ModulUltrasons
from movement.simulation_data import *
from movement.inverse_kinematics.steps import position_steps
# Inicialització del bus I2C i la controladora PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz és l’estàndard per a servos

# Inicialitza els 10 primers canals com a servos
servos = []
for i in range(16):
    s = servo.Servo(pca.channels[i], min_pulse=500, max_pulse=2500)
    servos.append(s)


class Pota:
    def __init__(self, cadera, genoll,right,front):
        self.servo_up = cadera
        self.servo_down = genoll
        self.state = "sit"  # Estat inicial de la pota
        self.right = right  
        self.front = front
        self.old_state = "start"

    def set_new_position(self,t, inter_method='linear'):
        new_pos = position(self.state)
        old_pos = position(self.old_state)

        up = 0
        down = 0
        if self.right:
            up = lambda a : 90 - a
            down = lambda a : a
        else:
            up = lambda a : 90 + a
            down = lambda a : 180 - a
        
        correction_factor = (up, down)
        steps = int(t/0.1)

        pos_steps = position_steps(old_pos, new_pos, steps, inter_method, correction_factor)

        up_steps = [pos[0] for pos in pos_steps]
        down_steps = [pos[1] for pos in pos_steps]
        print(up_steps, down_steps)
        t1 = threading.Thread(target=new_angles, args=(self.servo_up,up_steps,t/steps))
        t1.start()
        
        t2 = threading.Thread(target=new_angles, args=(self.servo_down,down_steps,t/steps))
        t2.start()

        t1.join()
        t2.join()


    def up(self):
        #DEPRECATED
        pass

    def down(self, new_state):
        #DEPRECATED
        pass

    def forward(self):  
        self.set_state(forwards(self.state))

    def backward(self):
        self.set_state(backwards(self.state))
    
    def set_state(self, new_state):
        """Estableix un nou estat per a la pota."""
        assert new_state in position_states.keys(), "Invalid state"
        self.old_state = self.state
        self.state = new_state
    

class EstructuraPotes:
    """Classe per gestionar les potes del quadrúpede."""
    def __init__(self,ultrasons: ModulUltrasons=None):
        self.ultrasons:ModulUltrasons = ultrasons

        self.legs = [
            Pota(servos[10], servos[11], True,True),  # Pota 1
            Pota(servos[12], servos[13], False,True),  # Pota 2
            Pota(servos[2], servos[3], True, False),  # Pota 3
            Pota(servos[7], servos[6], False, False)   # Pota 4
        ]
        threads = []

        for leg in self.legs:
            t = threading.Thread(target=leg.set_new_position, args=(0.3,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    
    def set_body_state(self,text):
        for leg in self.legs:
            leg.set_state(text)    

    def set_position(self,text):
        for leg in self.legs:
            leg.set_state(text)
        threads = []
        for leg in self.legs:
            th = threading.Thread(target=leg.set_new_position, args=(0.3,))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()

    def body_forward(self):
        for leg in self.legs:
            leg.backward()

    def body_backward(self):
        for leg in self.legs:
            leg.forward()

    def body_upward(self):
        for leg in self.legs:
            leg.set_state("center")

    def body_downward(self):
        for leg in self.legs:
            leg.set_state("sit")
            
    def sit_hind_legs(self, t=0.2):
        """Sit using only the hind legs while front legs are raised."""
        
        # hind legs
        self.legs[2].set_state("sit_down")
        self.legs[3].set_state("sit_down")
        # raise front legs
        self.legs[0].set_state("up")
        self.legs[1].set_state("up")

        threads = []
        for leg in self.legs:
            th = threading.Thread(target=leg.set_new_position, args=(t,))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()
        
            
    def strech(self, t=0.2):
        """Sit using only the hind legs while front legs are raised."""
        
        # hind legs
        self.legs[2].set_state("up")
        self.legs[3].set_state("up")
        # raise front legs
        self.legs[0].set_state("front_zero")
        self.legs[1].set_state("front_zero")

        threads = []
        for leg in self.legs:
            th = threading.Thread(target=leg.set_new_position, args=(t,))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()
        

    def init_bot(self, t=0.2):
        for leg in self.legs:
            if leg.front:
                leg.set_state("front_zero")
            else:
                leg.set_state("back_zero")
    
        threads = []
        for leg in self.legs:
            th = threading.Thread(target=leg.set_new_position, args=(t,))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()

    #set_positions
    def get_states(self):
        return [leg.state for leg in self.legs]

    """def follow_order(self, order, states, t=1):"""
    def follow_order(self, order,states = None, t=1):
        legs = self.legs
        inter_method = 'linear'

        direction, leg_n, method = order
        
        if method == 'p':
            inter_method = 'parabolic'

        #BODY
        if leg_n == 4:
            if   direction == 'f': 
                self.body_forward()
            elif direction == 'b': 
                self.body_backward()
            elif direction == 'u': 
                self.body_upward()
            elif direction == 'd': 
                self.body_downward()
        
        #LEG
        elif type(leg_n) == int:

            leg = legs[leg_n]
            legs = [leg]

            if direction ==  'f': 
                leg.forward()
            elif direction ==  'b':
                leg.backward()
            elif direction == 'ff':
                leg.forward()
                leg.forward()
        else:
            legs = [legs[i] for i in leg_n]
            for leg in legs:
                leg.set_state(direction)

        new_states = self.get_states()

        #Function move Body
        threads = []
        for leg in legs:
            th = threading.Thread(target=leg.set_new_position, args=(t,inter_method))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()
        return new_states

    def follow_sequance(self, sequance, cycles=1, t = 1):
        """states = self.init_bot()"""
        states = self.get_states()
        print(f"Initial states: {states}")

        for order in sequance["start"]:
            states = self.follow_order(order, states, t)
            print(f"After order {order}: {states}")
        
        for _ in range(cycles):
            for order in sequance["cycle"]:
                #if self.ultrasons and self.ultrasons.mesura_distancia() > config.LLINDAR_ULTRASONIC:
                states = self.follow_order(order, states, t)
                print(f"After order {order}: {states}")
            
        for order in sequance["end"]:
            states = self.follow_order(order, states, t)
            print(f"After order {order}: {states}")
        
        print(f"Final states: {states}")

def get_angle(state,right):
    (up, down) = position(state)
    if right:
        up = 90 - up
        down = down
    else:
        up = 90 + up
        down = 180 - down
    return (up,down)

def new_angle(servo,angle_final,angle_inicial, duracio, passos=30):
    pas = (angle_final - angle_inicial) / passos
    delay = duracio / passos

    for i in range(passos + 1):
        angle_actual = angle_inicial + i * pas
        servo.angle = max(0, min(180, angle_actual))  # Protecció límits
        time.sleep(delay)

def new_angles(servo,angles, delay):
    for angle in angles:
        servo.angle = max(0, min(180, angle))  # Protecció límits
        time.sleep(delay)

# Crear potes (ajusta els canals segons com els tinguis connectats)

def set_servo_angle(index, angle):
    """Posa un servo concret a un angle determinat."""
    if not (0 <= index < len(servos)):
        raise ValueError("Index de servo fora de rang.")
    if not (0 <= angle <= 180):
        raise ValueError("L'angle ha de ser entre 0 i 180 graus.")
    servos[index].angle = angle

def sweep_servo(index, delay=0.01):
    """Mou el servo d'un extrem a l'altre per provar el rang complet."""
    if not (0 <= index < len(servos)):
        raise ValueError("Index de servo fora de rang.")

    # Anada: de 0 a 180 graus
    for angle in range(0, 181, 1):
        servos[index].angle = angle
        time.sleep(delay)

    # Tornada: de 180 a 0 graus
    for angle in range(180, -1, -1):
        servos[index].angle = angle
        time.sleep(delay)

def mou_cap(index=15, temps_gir=0.4, pausa=0.2, intensitat=30):
    """
    Mou un servo de 360° des de posició aturada cap a dreta i esquerra.

    - intensitat: valor entre 0 i 90 (es suma/resta a 90)
      Ex: intensitat=30 → 120 dreta, 60 esquerra
    """
    # DRETA
    servos[index].angle = 94 + intensitat
    time.sleep(temps_gir)
    servos[index].angle = 94
    time.sleep(pausa)

    # ESQUERRA
    servos[index].angle = 94 - intensitat
    time.sleep(temps_gir)
    servos[index].angle = 94
    time.sleep(pausa)


def test_aturada(servo = servos[15]):
    print("Buscant el punt d’aturada...")
    for angle in range(85, 96):  # Prova valors entre 85 i 95
        servo.angle = angle
        print(f"Provat angle: {angle}")
        time.sleep(1)
        servo.angle = 94  # pausa entre intents
        time.sleep(0.3)

servos[15].angle = 94  # pausa entre intents
