import time
from heart import Heart
from distanceSensor import UltrasonicSensor

class Robot:

    # no enums in CircuitPython
    class RobotState:
        MONITOR = 1
        BEAT = 2,
        #OFF = 3

    def __init__(self, heart_beat_display:Heart, 
                 sensor:UltrasonicSensor, 
                 detection_threshold_mm=110):
        self.heart = heart_beat_display
        self.ultrasonic_sensor = sensor
        self.detection_threshold_mm = detection_threshold_mm
        self.robot_state = Robot.RobotState.MONITOR
        # make these additional parameters? 
        self.monitor_ramp_delay_seconds  = 0.015
        self.off_time_seconds = 0.1 
        self.distance = None

    def monitor(self) -> float:
        """Keep monitoring the distance. Transition to RAMPUP state if an object is detected."""
        distance_mm = self.ultrasonic_sensor.get_distance()
        # print(f'initial distance: {distance_mm}')
        # a = 0
        while distance_mm > self.detection_threshold_mm:
            time.sleep(self.monitor_ramp_delay_seconds)
            distance_mm = self.ultrasonic_sensor.get_distance()
            # a += 1
            # print('.', end='')
            # if a > 80:
            #     a = 0
            #     print()
        return distance_mm

    # TODO: off should move to Heart object
    #def turn_off(self):
    #    """Turn off the display and transition back to MONITOR."""
    #    time.sleep(self.off_time_seconds)
    #    self.robot_state = Robot.RobotState.MONITOR

    def trigger_heartbeat(self, distance_mm):
        self.heart.trigger_1_beat(distance_mm)
        
    

    
     # TODO change control of heartbeat to Heart Object
     # Robot object should not need to care about rampup/rampdown, just activate a heartbeat
     # ideally, we may want to just send a BPM to Heart object and then stop when distance out of range


    def run(self):
        """Main loop to manage state transitions."""
        while True:
            if self.robot_state == Robot.RobotState.MONITOR:
                # print('   STATE: MONITOR')
                self.distance = self.monitor()
                self.robot_state = Robot.RobotState.BEAT
            elif self.robot_state == Robot.RobotState.BEAT:
                # print('   STATE: BEAT')
                self.trigger_heartbeat(self.distance)
                self.robot_state = Robot.RobotState.MONITOR
            else:
                print('should not get here')
            #elif self.robot_state == Robot.State.OFF:
            #    self.turn_off()
