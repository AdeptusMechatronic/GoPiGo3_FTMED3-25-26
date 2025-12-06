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
    
        self.MAX_SPEED = 300 # Maks hastighet motor [DPS]
    
    def execute_outputs(self):

        # Henter ønsket hastighet og styring fra delt data
        speed = self.data.target_speed
        steering = self.data.target_steering    

        # Sikkerhetskontroll - begrens verdier
        speed = self._clamp(speed, -self.MAX_SPEED, self.MAX_SPEED)
        steering = self._clamp(steering, -100, 100) 

        # GoPiGo3 motor kontroll
        # Venstre motor: speed + steering (svinger høyre)
        # Høyre motor: speed - steering (svinger venstre)
        left_dps = speed + steering
        right_dps = speed - steering

        try:
            self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT, left_dps)
            self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT, right_dps)
        except Exception as e:
            print(f"Feil ved setting av motorhastighet: {e}")
    
    def _clamp(self, value, min_val, max_val):
        """Begrenser verdi innenfor min og max"""
        return max(min_val, min(max_val, value))
        
        pass
    
    def cleanup(self):
        self.gpg.stop()
