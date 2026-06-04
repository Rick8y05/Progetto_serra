import threading
import time

# classe che gestisce la simulazione del tempo nel sistema
class GestoreTempo:
    def __init__(self, gestore_serra, intervallo: float):
        self.gestore_serra = gestore_serra
        self.intervallo = intervallo
        self.conta_cicli = 0
        self.simulazione_attiva = False
        self.thread_tempo = None

    # ciclo principale di simulazione temporale
    def loop_tempo(self):
        #while non è invalidante, gira separatamente da tutto il resto grazie a tred
        while self.simulazione_attiva:
            time.sleep(self.intervallo)  # time slep non invalida perche gira separatamente da tutto il resto
            self.conta_cicli +=1
            # effettua chiamata aggiornamento sensori ogni tot. tempo
            self.gestore_serra.simulazione_aggiornamento_sensori()
            self.gestore_serra.controllo_periodico()

    # chiamata per avviare il loop ad inzio simulazione
    def avvia(self):
        if not self.simulazione_attiva:
            self.simulazione_attiva = True
            self.thread_tempo = threading.Thread(target=self.loop_tempo, daemon=True)
            # la riga sopra con target serve a dire "hai creato il ciclo di lavoro alternativo" e deve fare self.loop_tempo, è un puntatore)
            # "daemon" serve per dire "se il main principale va in arresto, fermati"
            # di default è su false e metterlo su true è una sicurezza in più anche se abbiamo fatto esci
            self.thread_tempo.start()

    # chiusura loop fine simulazione
    def ferma(self):
            self.simulazione_attiva = False
