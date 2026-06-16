# definizione della classe Attuatori che rappresenta un attuatore della serra (irrigatore, ventilatore, luce UV)
class Attuatori:
    def __init__(self,tipo: str, stato: bool):
        self.tipo = tipo
        self.stato = stato
    # restituisce lo stato corrente dell'attuatore
    @property
    def _stato(self):
        return self.stato
    # restituisce il tipo dell'attuatore
    @property
    def _tipo(self):
        return self.tipo
    # accende l'attuatore impostando lo stato = True
    def accendi(self):
        self.stato = True
    # spegnere l'attuatore impostando lo stato = False
    def spegni(self):
        self.stato = False
