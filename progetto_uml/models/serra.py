from models.sensore import Sensori
from models.attuatori import Attuatori

class Serra:
    def __init__(
        self,
        proprietario: str,
        dati_coltura: dict,
        modalita: str,
        path_temperature: str,
        path_umidita: str,
        codice_univoco: str,
        nome_pianta: str,
    ):
        self.codice_univoco = codice_univoco
        self.proprietario = proprietario
        self.nome_pianta = nome_pianta
        self.modalita = modalita.strip().lower() if isinstance(modalita, str) else "manuale"
        self.pianta_selezionata = dati_coltura or {"temperatura": 20, "umidita": 50}
        self.path_temperature = path_temperature
        self.path_umidita = path_umidita

        self.T1 = Sensori("temperatura", self.path_temperature)
        self.U1 = Sensori("umidita", self.path_umidita)
        self.temperatura_serra = self.T1.get_dati()
        self.umidita_serra = self.U1.get_dati()

        self.ventole_attuatore = Attuatori("ventole_aereazione", False)
        self.sistema_irrigazione_attuatore = Attuatori("sistema_irrigazione", False)
        self.lampada_uv_attuatore = Attuatori("lampadaUV", False)

        self.ventole = False
        self.irrigazione = False
        self.lampada_uv = False

    def mod_automatica(self):
        self.temperatura_serra = self.T1.get_dati()
        self.umidita_serra = self.U1.get_dati()

        if self.pianta_selezionata is None:
            self.pianta_selezionata = {"temperatura": 20, "umidita": 50}

        if self.temperatura_serra > self.pianta_selezionata["temperatura"]:
            self.ventole_attuatore.accendi()
            self.ventole = True
        else:
            self.ventole_attuatore.spegni()
            self.ventole = False

        if self.temperatura_serra < self.pianta_selezionata["temperatura"]:
            self.lampada_uv_attuatore.accendi()
            self.lampada_uv = True
        else:
            self.lampada_uv_attuatore.spegni()
            self.lampada_uv = False

        if self.umidita_serra < self.pianta_selezionata["umidita"]:
            self.sistema_irrigazione_attuatore.accendi()
            self.irrigazione = True
        else:
            self.sistema_irrigazione_attuatore.spegni()
            self.irrigazione = False

    def mod_manuale_ventole(self, stato: bool):
        if stato:
            self.ventole_attuatore.accendi()
        else:
            self.ventole_attuatore.spegni()
        self.ventole = bool(stato)

    def mod_manuale_lampada_uv(self, stato: bool):
        if stato:
            self.lampada_uv_attuatore.accendi()
        else:
            self.lampada_uv_attuatore.spegni()
        self.lampada_uv = bool(stato)

    def mod_manuale_sistema_irrigazione(self, stato: bool):
        if stato:
            self.sistema_irrigazione_attuatore.accendi()
        else:
            self.sistema_irrigazione_attuatore.spegni()
        self.irrigazione = bool(stato)

    @property
    def get_temperatura_serra(self) -> float:
        return self.temperatura_serra

    @property
    def get_umidita_serra(self) -> float:
        return self.umidita_serra

    @property
    def get_stato_ventole(self):
        return self.ventole

    @property
    def get_stato_lampadaUV(self):
        return self.lampada_uv

    @property
    def get_stato_lampada_uv(self):
        return self.lampada_uv

    @property
    def get_stato_sistema_irrigazione(self):
        return self.irrigazione

    def set_coltura(self, dati_coltura: dict, nome_pianta: str = None):
        self.pianta_selezionata = dati_coltura or {"temperatura": 20, "umidita": 50}
        if nome_pianta:
            self.nome_pianta = nome_pianta

    def set_ventole(self, stato: bool):
        self.ventole = bool(stato)

    def set_irrigazione(self, stato: bool):
        self.irrigazione = bool(stato)

    def set_lampada_uv(self, stato: bool):
        self.lampada_uv = bool(stato)

# Le serre utilizzano i dati della coltura forniti da GestoreColture.
# L'oggetto Serra mantiene lo stato di sensori e attuatori per ogni codice univoco.



#postilla le serre accedono a tutte le coture dunque non bisogna mandargli direttamente i dati basta mandargli
# il nome della pianta, dunque il flow è gestore colture trova se ce quella pianta, manda a gestore serre
#che punta a quella precisa serra e gli ivia
#sentire al prof per quanto riguarda il fatto della repository dentro ogni serra
