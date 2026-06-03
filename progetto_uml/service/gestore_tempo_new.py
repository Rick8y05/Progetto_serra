# gestore tempo

import threading
import time


class GestoreTempo:
    # Gestore di simulazione e aggiornamento dei sensori delle serre.
  

    def __init__(self, gestore_serra, intervallo=10):
        
        self.gestore_serra = gestore_serra
        self.intervallo = intervallo
        self.attivo = False
        self.thread_simulazione = None

    def avvia(self):
        if not self.attivo:
            self.attivo = True
            self.thread_simulazione = threading.Thread(target=self._esegui_ciclo, daemon=True)
            self.thread_simulazione.start()
            print("OK: Simulazione sensori avviata")

    def ferma(self):
        self.attivo = False
        if self.thread_simulazione:
            self.thread_simulazione.join(timeout=2)
        print("OK: Simulazione sensori fermata")

    def _esegui_ciclo(self):
        while self.attivo:
            try:
                # Esegue l'aggiornamento automatico delle serre
                for n_univoco, serra in self.gestore_serra.serre_attive.items():
                    if serra.modalita.lower() == "automatica":
                        serra.mod_automatica()
                
                # Attende prima del prossimo aggiornamento
                time.sleep(self.intervallo)
            except Exception as e:
                print(f"AVVISO: Errore nel ciclo di simulazione: {e}")
                continue

    def set_intervallo(self, intervallo):
        self.intervallo = intervallo
