from models.sensore import Sensori
from models.attuatori import Attuatori
class Serra:
    def __init__ (self,proprietario: str,coltura_attiva: dict, modalita: str,dati_temperature, dati_umidita, codice_univoco: str, nome_pianta: str):
        self.nome_pianta = nome_pianta
        self.codice_univoco = codice_univoco
        self.proprietario = proprietario
        self.coltura_attiva = coltura_attiva #indirizzo memoria dati cooltura
        self.modalita= modalita
        self.dati_temperature = dati_temperature
        self.dati_umidita = dati_umidita
        #creazione sensori specifici per questa istanza di serra
        self.T1 = Sensori("temperatura",self.dati_temperature)
        self.U1 = Sensori("umidità",self.dati_umidita)
        self.temperatura_serra=self.T1.get_dati()
        self.umidita_serra=self.U1.get_dati()
        self.ventole=Attuatori("ventole_aereazione", False)
        self.sistema_irrigazione = Attuatori("sistema_irrigazione", False)
        self.lampada_UV = Attuatori("lampadaUV", False)
    def mod_automatica(self):
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
        if stato:
            self.ventole.accendi()
        else: self.ventole.spegni()
    def mod_manuale_lampada_UV(self,stato: bool):
        if stato:
            self.lampada_UV.accendi()
        else:
            self.lampada_UV.spegni()
    def mod_manuale_sistema_irrigazione(self,stato: bool):
        if stato:
            self.sistema_irrigazione.accendi()
        else:
            self.sistema_irrigazione.spegni()
    @property
    def get_temperatura_serra(self) -> float:
        self.temperatura_serra = self.T1.get_dati()
        return self.temperatura_serra
    @property
    def get_umidita_serra(self) -> float:
        self.umidita_serra = self.U1.get_dati()
        return self.umidita_serra
    @property
    def get_dati_coltura(self) -> dict: #dict type Hint per dizionario
        return self.coltura_attiva
    @property
    def get_stato_ventole(self):
        return self.ventole._stato
    @property
    def get_stato_lampadaUV(self):
        return self.lampada_UV._stato
    @property
    def get_stato_sistema_irrigazione(self):
        return self.sistema_irrigazione._stato
    def set_coltura(self,coltura_attiva,pianta):
        self.coltura_attiva = coltura_attiva
        self.nome_pianta = pianta


#postilla le serre accedono a tutte le coture dunque non bisogna mandargli direttamente i dati basta mandargli
# il nome della pianta, dunque il flow è gestore colture trova se ce quella pianta, manda a gestore serre
#che punta a quella precisa serra e gli ivia
#sentire al prof per quanto riguarda il fatto della repository dentro ogni serra
