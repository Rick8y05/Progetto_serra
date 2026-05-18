from models.sensore import Sensori
from repository.lettore_dati import DatiRepository
from models.attuatori import Attuatori
class Serra:
    def __init__ (self,proprietario: str,path_dati_coltura: str, modalita: str,path_temperature: str, path_umidita: str, codice_univoco: str):
        self.codice_univoco = codice_univoco
        self.pianta_selezioanta: dict = None #dizionario dati coltura selezionata
        self.proprietario = proprietario
        self.path_dati_coltura = path_dati_coltura #indirizzo memoria dati cooltura
        self.dati_coltura = DatiRepository(self.path_dati_coltura, dict).get_dati #dizionario di dizionari, sono presenti tutte le colture
        self.modalita= modalita
        self.path_temperature = path_temperature
        self.path_umidita = path_umidita
        #creazione sensori specifici per questa istanza di serra
        self.T1 = Sensori("temperatura",self.path_temperature)
        self.U1 = Sensori("umidità",self.path_umidita)
        self.temperatura_serra=self.T1.get_dati()
        self.umidita_serra=self.U1.get_dati()
        self.ventole=Attuatori("ventole_aereazione", False)
        self.sistema_irrigazione = Attuatori("sistema_irrigazione", False)
        self.lampada_UV = Attuatori("lampadaUV", False)
    def mod_automatica(self):
        self.temperatura_serra = self.T1.get_dati()
        self.umidita_serra = self.U1.get_dati()
        if self.pianta_selezioanta==None:
            self.pianta_selezioanta = self.set_coltura("basilico")
        if self.temperatura_serra>self.pianta_selezioanta["temperatura"]:
            self.ventole.accendi()
        else:
            self.ventole.spegni()
        if  self.temperatura_serra< self.pianta_selezioanta["temperatura"]:
            self.lampada_UV.accendi()
        else:
            self.lampada_UV.spegni()
        if self.umidita_serra< self.pianta_selezioanta["umidita"]:
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
        return self.temperatura_serra
    @property
    def get_umidita_serra(self) -> float:
        return self.umidita_serra
    @property
    def get_dati_coltura(self) -> dict: #dict type Hint per dizionario
        return self.dati_coltura
    @property
    def get_stato_ventole(self):
        return self.ventole
    @property
    def get_stato_lampadaUV(self):
        return self.lampada_UV
    @property
    def get_stato_sistema_irrigazione(self):
        return self.sistema_irrigazione
    def set_coltura(self,nome_pianta: str):
        try:
            nome_pulito = nome_pianta.lower() #serve in caso limbecille che usa il pc scrive con maiuscole il nome
            self.pianta_selezioanta = self.dati_coltura[nome_pulito]

        except KeyError:
            print("Pianta non trovata in memoria dati")



