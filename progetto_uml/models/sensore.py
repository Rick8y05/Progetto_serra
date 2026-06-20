from repository.lettore_dati import DatiRepository


class Sensori:
    """
    SIMULAZIONE SENSORI
    """
    def __init__(self, tipo: str, dati):
        """
        Inizializzazione sensori
        """
        self._tipo = tipo
        self.dati = dati
        self.indice_corrente = 0
        self.valore_attuale = self.dati[self.indice_corrente]

    
    def get_dati(self):
        """
        Restituisce il valore attualmente rilevato dal sensore
        """
        return self.valore_attuale

    # property per ottenere il tipo del sensore
    @property
    def tipo(self) -> str
    """
    Metodo per ottenere il tipo del sensore
    """
        return self._tipo

    
    def aggiornamento_sensore(self):
        """
        Aggiorna il valore corrente del sensore avanzando nell'indice dei dati
        """
        self.indice_corrente += 1
        if self.indice_corrente >= len(self.dati):
            self.indice_corrente = 0
        self.valore_attuale = self.dati[self.indice_corrente]
