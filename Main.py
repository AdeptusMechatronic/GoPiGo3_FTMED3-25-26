"""
Hovedprogram
Importerer sensordata og logikk,
Aktiverer funksjoner i rett rekkefolge
"""
import easygopigo3 as gpg
import time
from Minne import SensorData
from Styring import Logikk
from Innganger import InputHandler
from Utganger import Utganger

def main():
    print("Starter opp")
    

    # Initialisering av data
    delt_data = SensorData()
    
    try:
        robot_hardware = gpg.EasyGoPiGo3()
    except Exception as e:
        print(f"Feil ved initialisering av GoPiGo {e}")
        print("Sjekk om GoPiGo er tilkoblet")
        return #Avslutter hvis feil

    # Oppretter objekter. Sender data til inngang og utgang moduler
    input_handler = InputHandler(delt_data, robot_hardware)
    output_handler = Utganger(delt_data, robot_hardware)
    logikk = Logikk(delt_data)
    
    
    """ Main task """
    
    try:
        while True:
            # Henter data fra innganger
            input_handler.read_and_update_all()
            
            # Logikk
            logikk.handling()
            
            # Utganger
            output_handler.execute_outputs()
            
            # Pusterom
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Avslutter program")
        
    finally:
        # Opprydding
        Utganger.cleanup() # sikrer at motorer stopper
        InputHandler.cleanup() # renser GPIO
        print("Program avsluttet")
        
if __name__ == "__main__":
    main()
