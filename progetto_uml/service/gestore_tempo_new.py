# services/gestore_tempo.py

import threading
import time


class GestoreTempo:
    """
    Gestore del ciclo di simulazione e aggiornamento dei sensori delle serre.
    Esegue gli aggiornamenti in un thread separato per non bloccare l'interfaccia grafica.
    """

    def __init__(self, gestore_serra, intervallo=10):
        """
        Args:
            gestore_serra: Istanza di GestoreSerra
            intervallo: Intervallo in secondi tra gli aggiornamenti dei sensori (default 10s)
        """
        self.gestore_serra = gestore_serra
        self.intervallo = intervallo
        self.attivo = False
        self.thread_simulazione = None

    def avvia(self):
        """Avvia il thread di simulazione dei sensori"""
        if not self.attivo:
            self.attivo = True
            self.thread_simulazione = threading.Thread(target=self._esegui_ciclo, daemon=True)
            self.thread_simulazione.start()
            print("OK: Simulazione sensori avviata")

    def ferma(self):
        """Arresta il thread di simulazione"""
        self.attivo = False
        if self.thread_simulazione:
            self.thread_simulazione.join(timeout=2)
        print("OK: Simulazione sensori fermata")

    def _esegui_ciclo(self):
        """Esegue il ciclo di simulazione (eseguito nel thread separato)"""
        while self.attivo:
            try:
                # Esegui l'aggiornamento automatico delle serre
                for n_univoco, serra in self.gestore_serra.serre_attive.items():
                    if serra.modalita.lower() == "automatica":
                        serra.mod_automatica()
                
                # Attendi prima del prossimo aggiornamento
                time.sleep(self.intervallo)
            except Exception as e:
                print(f"AVVISO: Errore nel ciclo di simulazione: {e}")
                continue

    def set_intervallo(self, intervallo):
        """Modifica l'intervallo di aggiornamento"""
        self.intervallo = intervallo
