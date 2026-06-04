from repository.lettore_dati import DatiRepository

# definizione della classe Sensori che rappresenta un sensore della serra che legge valori da una lista di dati
class Sensori:
    def __init__(self, tipo: str, dati):
        self._tipo = tipo
        self.dati = dati
        self.indice_corrente = 0
        self.valore_attuale = self.dati[self.indice_corrente]

    # restituisce il valore attualmente rilevato dal sensore
    def get_dati(self):
        return self.valore_attuale

    # property per ottenere il tipo del sensore
    @property
    def tipo(self) -> str:
        return self._tipo

    # aggiorna il sensore
    def aggiornamento_sensore(self):
        # Incrementa l'indice
        self.indice_corrente += 1

        # Controllo di sicurezza: se esce dal range, resetta a zero
        if self.indice_corrente >= len(self.dati):
            self.indice_corrente = 0

        # Aggiorna il valore attuale
        self.valore_attuale = self.dati[self.indice_corrente]
