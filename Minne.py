"""
Lagring av sensordata og kontrolldata for utganger
"""

import time


class SensorData:

    def __init__(self):
    
        """ Innganger """
        
        # Avstandssensorer
        self.distance_L = 0.0 # Avstand i cm, venstre sensor
        self.distance_R = 0.0 # Avstand i cm, høyre sensor
        
        # Start/stopp knapp (ssPin)
        self.button_state = False # True = knapp trykket
        
        """ Utganger (motorhastighet etc) """
        
        # Motorer
        self.target_speed = 0 # Felles hast for begge motorer
        self.target_steering = 0 # Styresignal: -100 (venstre) til 100 (høyre)
        
        
        """ Tilstander (start/stopp, sitter fast etc) """
        
        self.current_state = "STOPPET" # Tilstand satt ved oppstart
       
