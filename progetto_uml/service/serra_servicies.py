from repository.lettore_dati import DatiRepository
from models.serra import Serra
class GestoreSerra:
    def __init__ (self,path_raccolta_serre: str, path_dati_colture: str, path_temperature: str, path_umidita: str):
        self.path_temperature = path_temperature
        self.path_umidita = path_umidita
        self.path_dati_colture = path_dati_colture
        self.path_raccolta_serre = path_raccolta_serre
        self.dati_serra: dict = DatiRepository(self.path_raccolta_serre, dict).get_dati# tutti i dati reltivi alle singole serre
        #dizionario di dizionari organizzato per codice univoco con sotto tutto per creare serra
        self.serre_attive=[]#lista per mantenere vivi gli oggetti serra
        for n_univoco, info_serra in self.dati_serra.items():
            serra_attivata=Serra(info_serra["proprietario"],path_dati_colture,info_serra["modalita"],self.path_temperature, self.path_umidita,n_univoco) #attiva una delle serre salvate
            self.serre_attive.append(serra_attivata)#la mette dentro una lista di serre per mantenerla salvata
        # definire gestione_parco_serre
    def visualizza_stato_serre(self,n_univoco):
        umidita=self.serre_attive[n_univoco].get_umidita_serra
        temperatura=self.serre_attive[n_univoco].get_temperatura_serra
        stato_ventole=self.serre_attive[n_univoco].get_stato_ventole_serra
        stato_impianto_irrigazione=self.serre_attive[n_univoco].get_stato_impianto_irrigazione
        stato_lampada_uv=self.serre_attive[n_univoco].get_stato_lampadauv
        return [umidita,temperatura,stato_ventole,stato_impianto_irrigazione,stato_lampada_uv]
    def verifica_esistenza_serra(self):#controlla che il codice univoco sia oresente
    #gestoreParcoSerra ricordarsi di mettere controolo con try except
        pass



class SerraService:

    def __init__(self, path_serre, path_colture, path_temperature, path_umidita):

        self.path_serre = path_serre
        self.path_colture = path_colture
        self.path_temperature = path_temperature
        self.path_umidita = path_umidita

        self.repo_serre = DatiRepository(self.path_serre, dict)
        self.dati_serre = self.repo_serre.get_dati or {}

        self.serre = {}

        for codice, info in self.dati_serre.items():

            codice = codice.strip().lower()

            self.serre[codice] = Serra(
                info.get("proprietario"),
                info.get("coltura", "default"),
                info.get("modalita", "manuale"),
                self.path_temperature,
                self.path_umidita,
                codice
            )

    def get_serra(self, codice):
        return self.serre.get(codice.strip().lower())
    
    def configura_coltura(self, codice_serra, coltura):
        serra = self.get_serra(codice_serra)
        if not serra:
            print("Serra non trovata")
            return
        serra.coltura = coltura

    def azione_manuale(self, codice, dispositivo, stato):

        serra = self.get_serra(codice)

        if not serra:
            print("SERRA NON TROVATA")
            return

        stato_bool = stato.lower() == "on"

        if dispositivo == "1":
            serra.set_ventole(stato_bool)
        elif dispositivo == "2":
            serra.set_irrigazione(stato_bool)
        elif dispositivo == "3":
            serra.set_lampada_uv(stato_bool)
        else:
            print("Dispositivo non valido")

        print("OK")

    def set_modalita(self, modalita):
        for s in self.serre.values():
            s.modalita = "automatica" if modalita == "1" else "manuale"

    def esegui_ciclo_automatico(self):
        for s in self.serre.values():
            s.mod_automatica()

    def leggi_stato_serra(self, codice):
        serra = self.get_serra(codice)

        if not serra:
            return None

        return serra
    
    def get_dati_plancia(self):
        serra = self.repository.get_serra_attiva()

        if serra is None:
            return None

        return {
            "ventole": serra.ventole,
            "irrigazione": serra.irrigazione,
            "lampada_uv": serra.lampada_uv,
            "temperatura": serra.temperatura_serra,
            "umidita": serra.umidita_serra,
            "coltura": serra.coltura
        }


