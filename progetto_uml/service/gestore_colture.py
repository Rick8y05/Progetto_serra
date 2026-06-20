
class GestoreColture:
    def __init__(self, dati_colture: dict , dati_colture_utente: dict ):
        """
        INIZIALIZZAZIONE GESTORE COLTURE
        """
        self.dati_colture = dati_colture
        self.dati_colture_utente = dati_colture_utente
        
    
    def aggiornamento_parametri_catalogo(self, pianta, tipo_parametro, nuovo_dato):
        """
        Metodo per il cambio di un parametro di una coltura specifica
        """
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

   
    @property
    def get_catalogo_aggiornato(self):
        """
        Getter per vedere il catalogo aggiornato
        """
        return self.dati_colture

    
    def configurazione_parametri_coltura(self,pianta: str):
        """
        Metodo in cui il proprietario prende i dati dal software e li inserisce nella serra per mod. automatica
        """
        try:
            return self.dati_colture[pianta]
        except KeyError:
            print(f"la pianta {pianta} non è presente nel catalogo")
            return None

    
    def caricamento_dati_fenotipici(self,pianta:str, proprietario: str, busto: float, altezza: float, impostazioni: bool):
        """
        Metodo con cui il proprietario inserisce i nuovi dati fenotipici per la pianta 
        """
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
        """
        Metodo per la rimozione dei dati caricati da un proprietario nel file dati colture utente 
        """
        if proprietario in self.dati_colture_utente:
            self.dati_colture_utente.pop(proprietario)

    
    def colture_disponibili (self):
        """
        Metodo che restituisce le colture disponibili 
        """
        colture_disponibili = []
        for colture in self.dati_colture:
            colture_disponibili.append(colture)
        return colture_disponibili

