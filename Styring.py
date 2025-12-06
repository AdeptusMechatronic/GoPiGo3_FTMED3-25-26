"""
Styring av logikk for funksjoner
f.eks. start og stopp, sving etc
"""

from Minne import SensorData
import time
import math

class Logikk:
    """
    Logisk styring av utgangssignaler basert på tilbakemelding fra sensorer
    """
    
    def __init__(self, delt_data):
        self.data = delt_data
        
        # Terskel for hinderdeteksjon [cm]
        self.HINDER_DET = 20
        self.BLINDVEI_DET = 12
        
        # Konstante verdier
        self.HAST_FRAM = 150 # Default hast framover [DPS]
        self.STYRE_VERDI = 70 # Styrerespons ved navigasjon [0-100]   
        pass

    def handling(self):
        
        # Sjekk nåværende tilstand fra minne
        current_state = self.data.current_state
        
        #Leser avstand fra sensorer 
        dist_L = self.data.distance_L
        dist_R = self.data.distance_R
        
        """ Stopptilstand """
        
        if current_state == "STOPPET":
            # 0 hvis stoppet
            self.data.target_speed = 0
            self.data.target_steering = 0
        
            # Sjekk om startknapp er trykket
            if self.data.button_state == True:
                print("Går til kjøring")
                self.data.current_state = "Kjøring" #Endrer status i Minne
                self.data.target_speed = 100

                
            
        
        """ Tilstand kjøring """
        
        elif current_state == "Kjøring":
           
           # Sjekk blindvei/hindring front
           if dist_L < self.BLINDVEI_DET and dist_R < self.BLINDVEI_DET:
               print("Hindring, går til navigasjonsmodus")
               self._transition_to("Navigasjon")
               return
            
            
            # Sjekk for hinder som kan unngås
            elif dist_L < self.HINDER_DET or dist_R < self.HINDER_DET:
                # Beregner styring for å unngå hindring
                steering = self._calculate_avoidance_steering(dist_L, dist_R)
                self.data.target_steering = steering
                self.data.target_speed = self.HAST_FRAM
                return
       
       
           """ Tilstand navigasjon """
           
           elif current_state == "Navigasjon":
               print("Hindring funnet, leter etter trygg rute...")
               self.data.target_speed = -50
               self.data.target_steering = 100
               
               
               
               
           
           
           """ 
            """ Sjekker om det er hinder foran """
            # Ingen hinder, kjør framover
            if dist_L < 30 and dist_R < 30:
                self.data.current_state = "Navigasjon" #Skriver til minnet
                self.data.target_speed = 0
            else:
                # Fortsett å kjøre, men juster styring
                self.data.target_speed = 100
                self.data.target_steering = self._calculate_steering_adjustement()
    
    def _calculate_steering_adjustement(self):
    
    
                """ Håndtering av hinder """
                elif current_state == "Navigasjon":
                    if dist_L < HINDER_DET or dist_R < HINDER_DET:
                     
        
                        # Hindring høyre, klar bane venstre. Sving unna
                        if dist_L > dist_R:
                            steering = -70                
                
                        # Hindring venstre, klar bane høyre. Sving unna
                        elif dist_R > dist_L:
                            steering = 70
                
                        # Hindring begge sider, rygg og let etter åpning
                        else:
                            self.data.current_State = "Blindvei"
                            
                """ Handling ved blindvei """
                elif current_state == "Blindvei":
                """    
