# aggiornare parametri catalogo colture opeatore
# configurare parametri colture
from repository.lettore_dati import DatiRepository
class GestoreColture:
    def __init__(self, dati_colture: dict , dati_colture_utente: dict ):
        self.dati_colture = dati_colture
        self.dati_colture_utente = dati_colture_utente
    # sottometodo per il cabio di un parametro di una coltura specifica
    def aggiornamento_parametri_catalogo(self, pianta, tipo_parametro, nuovo_dato):
        try:
            controllo_valore = float(nuovo_dato)
        except (ValueError, TypeError):
            return False

        if tipo_parametro == "temperatura":
            if 0 < controllo_valore < 45 :
                self.dati_colture[pianta][tipo_parametro] = nuovo_dato
                return True
            else:
                return False
        else:
            if 0 < controllo_valore < 100 :
                self.dati_colture[pianta][tipo_parametro] = nuovo_dato
                return True
            else:
                return False

    # getter per vedere il catalogo aggiornato
    @property
    def get_catalogo_aggiornato(self):
        return self.dati_colture

    # metodo in cui il proprietario prende i dati dal software e li inserisce nella serra per mod. automatica
    def configurazione_parametri_coltura(self,pianta: str):
        try:
            return self.dati_colture[pianta]
        except KeyError:
            print(f"la pianta {pianta} non è presente nel catalogo")
            return None
    def caricamento_dati_fenotipici(self,pianta:str, proprietario: str, busto: float, altezza: float, impostazioni: bool):
        if pianta in self.dati_colture:
            dati_nuovi= {"pianta": pianta,
                         "busto": busto,
                         "altezza": altezza,
                         "imp_fabbrica": impostazioni}
            self.dati_colture_utente[proprietario] = dati_nuovi
            print("dati salvati correttamente")
        else:
            print("pianta non prensete nel catalogo")

    def rimuovi_dati_utente(self, proprietario: str):
        if proprietario in self.dati_colture_utente:
            self.dati_colture_utente.pop(proprietario)

    def colture_disponibili (self):
        colture_disponibili = []
        for colture in self.dati_colture:
            colture_disponibili.append(colture)
        return colture_disponibili

# comunica con gestore serra, gestore serra chima configura_parametri_coltura che gli invia
# solo i dati della pianta selezionata.
