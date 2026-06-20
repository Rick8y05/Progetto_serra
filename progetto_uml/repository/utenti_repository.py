import json
import os


class UtentiRepository:
"""
Classe dedicata alla persistenza dei dati utente su file JSON
"""
    def __init__(self):
        """
        INIZIALIZZAZIONE CLASSE 
        """
        
        self.path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "utenti.json")
        )

    
    def get_all(self):
        """
        Legge il file json con gli utenti
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

   
    def save_all(self, utenti):
        """
        Salva i dati degli utenti nel file json
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(utenti, f, indent=4, ensure_ascii=False)


    def get_path(self):
        """
        Restituisce il percorso del file utenti.json
        """
        return self.path
