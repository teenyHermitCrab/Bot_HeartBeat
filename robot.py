import time
from heart import Heart
from distance_sensor import UltrasonicSensor

class Robot:

    # no enums in CircuitPython
    class RobotState:
        MONITOR = 1
        BEAT = 2,
        #OFF = 3   OFF is now inside Heart class

    def __init__(self, heart_beat_display:Heart, 
                 sensor:UltrasonicSensor, 
                 detection_threshold_cm=110):
        self.heart = heart_beat_display
        self.ultrasonic_sensor = sensor
        self.detection_threshold_cm = detection_threshold_cm
        self.robot_state = Robot.RobotState.MONITOR
        # make these additional parameters? 
        self.monitor_ramp_delay_seconds  = 0.015
        self.off_time_seconds = 0.1 
        self.distance = None


    def monitor(self) -> float:
        """Keep monitoring the distance. Return distance if falls below threshold"""
        distance_cm = self.ultrasonic_sensor.get_distance()
        while distance_cm > self.detection_threshold_cm:
            time.sleep(self.monitor_ramp_delay_seconds)
            distance_cm = self.ultrasonic_sensor.get_distance()
        return distance_cm


    def trigger_heartbeat(self, distance_cm:float):
        self.heart.trigger_1_beat(distance_cm)
        
    

    
     # Robot object should not need to care about rampup/rampdown, just activate 
     # ideally, we may want to just send a BPM to Heart object


    def run(self):
        """Main loop to manage state transitions."""
        while True:
            if self.robot_state == Robot.RobotState.MONITOR:
                self.distance = self.monitor()
                self.robot_state = Robot.RobotState.BEAT
            elif self.robot_state == Robot.RobotState.BEAT:
                self.trigger_heartbeat(self.distance)
                self.robot_state = Robot.RobotState.MONITOR
            else:
                print('should not get here')
