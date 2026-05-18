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
        stato_lampadaUV=self.serre_attive[n_univoco].get_stato_lampadaUV
        return [umidita,temperatura,stato_ventole,stato_impianto_irrigazione,stato_lampadaUV]
    def verifica_esistenza_serra(self):#controlla che il codice univoco sia oresente
    #gestoreParcoSerra ricordarsi di mettere controolo con try except


