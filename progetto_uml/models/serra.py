from models.sensore import Sensori
from models.attuatori import Attuatori

class Serra:
    """ 
    CLASSE SERRA
    """
    def __init__ (self,proprietario: str,coltura_attiva: dict, modalita: str,dati_temperature, dati_umidita, codice_univoco: str, nome_pianta: str):
        """
        Inizializzazione classe serra
        """
        self.nome_pianta = nome_pianta
        self.codice_univoco = codice_univoco
        self.proprietario = proprietario
        self.coltura_attiva = coltura_attiva 
        self.modalita= modalita
        self.dati_temperature = dati_temperature
        self.dati_umidita = dati_umidita
        self.T1 = Sensori("temperatura",self.dati_temperature)
        self.U1 = Sensori("umidità",self.dati_umidita)
        self.temperatura_serra=self.T1.get_dati()
        self.umidita_serra=self.U1.get_dati()
        self.ventole=Attuatori("ventole_aereazione", False)
        self.sistema_irrigazione = Attuatori("sistema_irrigazione", False)
        self.lampada_UV = Attuatori("lampadaUV", False)
    
    
    def mod_automatica(self):
        """
        Algoritmo automatico per gestione serra
        """
        self.temperatura_serra = self.T1.get_dati()
        self.umidita_serra = self.U1.get_dati()
        if self.temperatura_serra>self.coltura_attiva["temperatura"]:
            self.ventole.accendi()
        else:
            self.ventole.spegni()
        if  self.temperatura_serra< self.coltura_attiva["temperatura"]:
            self.lampada_UV.accendi()
        else:
            self.lampada_UV.spegni()
        if self.umidita_serra< self.coltura_attiva["umidita"]:
            self.sistema_irrigazione.accendi()
        else:
            self.sistema_irrigazione.spegni()

    
    def mod_manuale_ventole(self,stato: bool):
        """
        Controllo manuale delle ventole della singola serra
        """
        if stato:
            self.ventole.accendi()
        else: self.ventole.spegni()

    
    def mod_manuale_lampada_UV(self,stato: bool):
        """
        Controllo manuale della lampada UV della singola serra
        """
        if stato:
            self.lampada_UV.accendi()
        else:
            self.lampada_UV.spegni()

    
    def mod_manuale_sistema_irrigazione(self,stato: bool):
        """
        Controllo manuale del sistema irrigazione della singola serra
        """
        if stato:
            self.sistema_irrigazione.accendi()
        else:
            self.sistema_irrigazione.spegni()

   
    @property
    def get_temperatura_serra(self) -> float:
        """
        Restituisce il valore di temperatura corrente della serra
        """
        return self.temperatura_serra

    
    @property
    def get_umidita_serra(self) -> float:
        """
        restituisce il valore di umidità corrente della serra
        """
        return self.umidita_serra

    
    @property
    def get_dati_coltura(self) -> dict: 
        """
        Restituisce i dati della coltura
        """
        return self.coltura_attiva
    
   
    @property
    def get_stato_ventole(self):
        """
        Restituisce lo stato delle ventole
        """
        return self.ventole._stato
   
    
    @property
    def get_stato_lampadaUV(self):
        """
        Restituisce lo stato della lampada UV
        """
        return self.lampada_UV._stato

    
    @property
    def get_stato_sistema_irrigazione(self):
        """
        Restituisce lo stato dell'irrigazione
        """
        return self.sistema_irrigazione._stato

    
    def set_coltura(self,coltura_attiva,pianta):
        """
        Aggiorna la coltura attiva e il nome della pianta associata alla serra
        """
        self.coltura_attiva = coltura_attiva
        self.nome_pianta = pianta

    
    def aggiornamento_sensori(self):
        """
        Aggiornamento dati sensori
        """
        self.T1.aggiornamento_sensore()
        self.U1.aggiornamento_sensore()
        self.temperatura_serra = self.T1.get_dati()
        self.umidita_serra = self.U1.get_dati()
