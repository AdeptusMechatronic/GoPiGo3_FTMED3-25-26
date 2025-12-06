"""
Styring av utganger til robot
"""

#import
from Minne import SensorData
import RPi.GPIO as GPIO
import time
import easygopigo3 as gpg

#object

class Utganger:
    def __init__(self, delt_data, robot_hardware):
        self.data = delt_data
        self.gpg = robot_hardware
    
        pass
    
    def execute_outputs(self):
        # Kalles inn i main for å sette motor
        self.gpg.set_motor_limits(speed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT, speed + steering)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT, speed - steering)
        
        pass
    
    def cleanup(self):
        self.gpg.stop()
        pass
