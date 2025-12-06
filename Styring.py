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
        self.HAST_FRAM = 150  # Default hast framover [DPS]
        self.STYRE_VERDI = 70  # Styrerespons ved navigasjon [0-100]
        
        # Navigasjon-tilstand
        self.nav_start_time = None
        self.nav_phase = "reversing"  # "reversing", "turning", "searching"

    def handling(self):
        """Hovedlogikk basert på GRAFCET-tilstander"""
        
        current_state = self.data.current_state
        dist_L = self.data.distance_L
        dist_R = self.data.distance_R
        
        # ========== STOPPET ==========
        if current_state == "STOPPET":
            self.data.target_speed = 0
            self.data.target_steering = 0
        
            if self.data.button_state:
                print("Går til Kjøring")
                self.data.current_state = "Kjøring"
                self.data.target_speed = 100
        
        # ========== KJØRING ==========
        elif current_state == "Kjøring":
            # Blindvei detektert?
            if dist_L < self.BLINDVEI_DET and dist_R < self.BLINDVEI_DET:
                print(f"Blindvei! L={dist_L:.1f}cm, R={dist_R:.1f}cm - Navigasjon startet")
                self.data.current_state = "Navigasjon"
                self.nav_start_time = time.time()
                self.nav_phase = "reversing"
                self.data.target_speed = -50
                self.data.target_steering = 0
            
            # Unngåbar hindring på én side?
            elif dist_L < self.HINDER_DET or dist_R < self.HINDER_DET:
                steering = self._calculate_avoidance_steering(dist_L, dist_R)
                self.data.target_steering = steering
                self.data.target_speed = self.HAST_FRAM
            
            # Normal kjøring
            else:
                self.data.target_speed = self.HAST_FRAM
                self.data.target_steering = 0
        
        # ========== NAVIGASJON ==========
        elif current_state == "Navigasjon":
            self._handle_navigation(dist_L, dist_R)
    
    def _handle_navigation(self, dist_L, dist_R):
        """
        Håndterer navigasjon når blindvei er detektert
        Faser: reversing → turning → searching → tilbake til Kjøring
        """
        current_time = time.time()
        elapsed = current_time - self.nav_start_time
        
        if self.nav_phase == "reversing":
            # Rygg i 2 sekunder
            if elapsed < 2.0:
                self.data.target_speed = -50
                self.data.target_steering = 0
                if elapsed < 0.5:
                    print("Rygger...")
            else:
                # Gå til sving
                self.nav_phase = "turning"
                self.nav_start_time = current_time
                print("Begynner å snu...")
        
        elif self.nav_phase == "turning":
            # Snu 90 grader ca 1.5 sekunder
            if elapsed < 1.5:
                self.data.target_speed = 30
                self.data.target_steering = 100
            else:
                # Gå til søking
                self.nav_phase = "searching"
                self.nav_start_time = current_time
                print("Søker ny rute...")
        
        elif self.nav_phase == "searching":
            # Søk etter åpning - kjør sakte framover
            self.data.target_speed = 80  # Saktere enn normal kjøring
            self.data.target_steering = 0
            
            # Hvis minst én sensor har fri vei
            if dist_L > self.BLINDVEI_DET + 5 or dist_R > self.BLINDVEI_DET + 5:
                print(f"Åpning funnet! L={dist_L:.1f}cm, R={dist_R:.1f}cm - Tilbake til Kjøring")
                self.data.current_state = "Kjøring"
                self.nav_phase = "reversing"
            
            # Sikkerhet: hvis den har søkt i for lang tid, gi opp
            if elapsed > 10:
                print("Søk timeout - tilbake til Kjøring")
                self.data.current_state = "Kjøring"
                self.nav_phase = "reversing"
    
    def _calculate_avoidance_steering(self, dist_L, dist_R):
        """
        Beregner styring for å unngå hindring på én side
        Styr mot siden med mest plass
        """
        if dist_L < dist_R:
            return self.STYRE_VERDI  # Styr høyre
        else:
            return -self.STYRE_VERDI  # Styr venstre
    
    def _transition_to(self, new_state):
        """Bytter til ny tilstand"""
        self.data.current_state = new_state