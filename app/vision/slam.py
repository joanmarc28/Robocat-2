import time
import threading

import config
from vision.camera import RobotCamera
from sensors.ultrasonic import ModulUltrasons
from movement.motors import EstructuraPotes
from movement.simulation_data import walk_states

try:
    """from slam.main_slam import SLAMSystem"""

    from external.pyslam.slam import VisualSlam
except Exception as e:  # pragma: no cover - library might not be available
    VisualSlam = None
    print("pyslam not installed: {}".format(e))

class AutonomousSLAM:
    """Basic SLAM driven autonomous movement controller."""

    def __init__(self, camera: RobotCamera | None = None):
        if VisualSlam is None:
            raise RuntimeError(
                "pyslam library is required for AutonomousSLAM to run"
            )

        self.camera = camera or RobotCamera()
        self.ultrasons = ModulUltrasons()
        self.legs = EstructuraPotes(self.ultrasons)
        self.slam = VisualSlam()
        self.running = False

    def process_frame(self):
        frame = self.camera.capture_frame()
        self.slam.track(frame)

    def step_movement(self):
        dist = self.ultrasons.mesura_distancia()
        if dist > config.LLINDAR_ULTRASONIC:
            self.legs.follow_sequance(walk_states, cycles=1, t=0.2)
        else:
            self.legs.follow_order(("move_body", "backward"), t=0.2)

    def run(self):
        self.running = True
        while self.running:
            self.process_frame()
            self.step_movement()
            time.sleep(0.01)

    def stop(self):
        self.running = False


def start_autonomous_slam():
    slam_controller = AutonomousSLAM()
    thread = threading.Thread(target=slam_controller.run, daemon=True)
    thread.start()
    return slam_controller


if __name__ == "__main__":
    controller = start_autonomous_slam()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()