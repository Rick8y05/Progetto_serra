import json
import os

class UtentiRepository:

    def __init__(self):
        self.path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "utenti.json")
        )

    # legge il file json
    def get_all(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    # salva i dati nel file json
    def save_all(self, utenti):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(utenti, f, indent=4, ensure_ascii=False)

    # restituisce il percorso del file utenti.json
    def get_path(self):
        return self.path
