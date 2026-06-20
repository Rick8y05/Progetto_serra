import json

# classe Repository per la gestione della lettura, scrittura e salvataggio dei dati su file JSON
class DatiRepository:
    def __init__(self, path: str,tipo_default=list):
        """
        INIZIALIZZAZIONE CLASSE DATI REPOSITORY
        """
        self.path = path
        self.dati = None
        self.tipo_default = tipo_default
       
       
    def read(self):
        """
        Metodo lettore, legge i dati nei file e li carica in memoria
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file) 
        # se il file non viene trovato, restituisce una struttura vuota
        except FileNotFoundError:
            print("Errore file non trovato ")
            return self.tipo_default()
        except json.decoder.JSONDecodeError:
            print("Formato file non valido")
            return self.tipo_default()

    
    @property
    def get_dati(self):
        """
        Getter che restituisce i dati aggiornati dal file
        """
        self.dati = self.read() 
        return self.dati

   
    def salvataggio_dati(self, dati): 
        """
        Salva i dati nel file JSON (sovrascrive il contenuto esistente)
        """
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(dati, file, indent=4)
            print("salvataggio effettuato con successo")
        except Exception as e:
            print(f"errore durante il salvataggio {e}")
