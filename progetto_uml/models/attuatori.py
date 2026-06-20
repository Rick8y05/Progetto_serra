
class Attuatori:
    """
    CLASSE ATTUATORI
    """
    def __init__(self,tipo: str, stato: bool):
        """
        Inizializzazione classe attuatori
        """
        self.tipo = tipo
        self.stato = stato
    
   
    @property
    def _stato(self):
        """
        Restituisce lo stato corrente dell'attuatore
        """
        return self.stato
    
   
    @property
    def _tipo(self):
        """
        Restituisce il tipo dell'attuatore
        """
        return self.tipo
   
    def accendi(self):
        """
        Accende attuatore
        """
        self.stato = True
   
    def spegni(self):
        """
        Spegne attuatore
        """
        self.stato = False
