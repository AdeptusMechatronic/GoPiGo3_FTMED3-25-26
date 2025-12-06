"""
Håndtering av input signaler
"""
#import
from Minne import SensorData
import RPi.GPIO as GPIO
import time
import easygopigo3 as gpg

#object

class InputHandler:
    def __init__(self, data_object, gpg_robot):
        self.DEBOUNCE_DELAY = 0.3
        self.data = data_object
        self.gpg = gpg_robot #referanse til gpg-objekt
        
        
        # Import av start/stoppknapp
        self.ssPin = 17 #Start/stopp knapp

        # Definering av GPIO pinner
        GPIO.setmode(GPIO.BCM) #Broadcom pinout
        GPIO.setup(self.ssPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Definerer pinne som inngang med pull-up motstand


        # Import av sensordata fra gopigo3
        # read distance_sensor
        self.ds_left = self.gpg.init_distance_sensor(port="AD1") # Avstandssensor venstre
        self.ds_right = self.gpg.init_distance_sensor(port="AD2") # Avstandssensor høyre


        if self.ds_left is None or self.ds_right is None:
            raise RuntimeError("Failed to initialize distance sensors")

        # Import av sensordata, Obstacle avoidance sensor
        # read bool value

        # Start/stopp bryter
        # toggling switch
        # Håndterer knapp True = ikke trykket False = trykket
        self.last_button_state = False
        self.last_press_time = time.time()


    def read_and_update_all(self):
    # Leser og oppdaterer sensordata
        try:
            #Knapp
            current_button_state = GPIO.input(self.ssPin) == GPIO.LOW #trykket inn
            current_time = time.time()
            
            if current_button_state and not self.last_button_state and (current_time - self.last_press_time > 0.3):
                self.data.button_state = True
                self.last_press_time = current_time
            else:
                self.data.button_state = False
                
            self.last_button_state = current_button_state
            
            #Avstandssensorer
            self.data.distance_L = self.ds_left.read()
            self.data.distance_R = self.ds_right.read()
        except Exception as e:
            print(f"Error reading sensors: {e}")
    

    def cleanup(self):
        GPIO.cleanup()
        self.gpg.stop()