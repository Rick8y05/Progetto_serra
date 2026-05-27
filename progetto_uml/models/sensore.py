from repository.lettore_dati import DatiRepository#cosi il codice viene più pulito
#rispetto a fare quando richiami il metodo lettore_dati.DatiRepository().get_dati
class Sensori:
    def __init__(self,tipo: str, path):
        #init è il costruttore serve per costruire l'oggetto della classe
        #self invece è la colla che attaccca i dati inviati all oggetto appena creato
        self.tipo = tipo
        self.path = path
        self.dati = DatiRepository(self.path,list).get_dati
        self.indice_corrente = 0 #indice per stampare un valore diverso ogni chiamata
    #def nuovo_valore(self):
#il self dentro serve per dire che la funziona parla del sensre stesso
#qua andrebbe messa la funzione che cambia il valore ogni 30 secondi implementare più avanti

    def get_dati (self):
        valore=self.dati[self.indice_corrente]
        self.indice_corrente = self.indice_corrente + 1
        if self.indice_corrente == len(self.dati):
            self.indice_corrente = 0
        return valore
    #@property  # con questo fai in modo che id non sia modificabile
    @property
    def get_tipo (self) -> str:
        return self.tipo


