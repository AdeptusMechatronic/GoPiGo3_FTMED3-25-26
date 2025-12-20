import easygopigo3 as gpg
import RPi.GPIO as GPIO
from time import sleep

# GPIO oppsett
GPIO.setmode(GPIO.BCM)
# Start/stopp knapp
START_STOP_PIN_BCM = 17
# Setter pinne som inngang og aktiverer pull-up motstand
GPIO.setup(START_STOP_PIN_BCM, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Opprett instans av roboten
# Starter kommunikasjon med GoPiGo HAT
rotte = gpg.EasyGoPiGo3() 

# Aktiverer sensorer
ds = rotte.init_distance_sensor(port="AD1") # Avstandssensor


"""
Tilstandsvariabel, start/stopp funksjon
"""
robot_running = False # Oppstart i stopp-tilstand
knapp_pressed_last = False # manuell debouncing

def toggle_state(): # Veksler tilstanden når knappen trykkes
    global robot_running
    robot_running = not robot_running #skifter tilstand
    if robot_running:
        print("Start: kjører framover")
        rotte.forward()
    else:
        print("Stopp")
        rotte.stop()

"""
Hovedprogram
"""
try:
    print("Programmet starter, trykk start")
    
    while True:
        # Les av avstandssensor
        avstand = ds.read()
        # Håndterer knapp True = ikke trykket False = trykket
        current_knapp_state = GPIO.input(START_STOP_PIN_BCM)
        
        if current_knapp_state == 0 and not knapp_pressed_last:
            toggle_state()
            knapp_pressed_last = True
            
        elif current_knapp_state == 1 and knapp_pressed_last:
            knapp_pressed_last = False
            
        # Håndtering av kjøring    
        if robot_running:
            print(f"Avstand til hinder: {avstand} cm")
    
            # Sensorlogikk
            if avstand < 20:  
                rotte.stop()
                robot_running = False
                
                
        sleep(0.5)
    
except KeyboardInterrupt:
    print("\nProgrammet avsluttes")
finally:
    rotte.stop()
    GPIO.cleanup()
    