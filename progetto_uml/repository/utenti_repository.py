import json
import os

# questa classe si occupa della gestione del file utenti.json, leggendo e scrivendo la lista degli utenti
class UtentiRepository:

    def __init__(self):
        """
        INIZIALIZZAZIONE CLASSE 
        """
        
        self.path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "utenti.json")
        )

    # legge il file json con gli utenti
    def get_all(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        # in caso di errore restituisce una lista vuota
        except:
            return []

    # salva i dati degli utenti nel file json
    def save_all(self, utenti):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(utenti, f, indent=4, ensure_ascii=False)

    # restituisce il percorso del file utenti.json
    def get_path(self):
        return self.path
