import json

# classe Repository per la gestione della lettura, scrittura e salvataggio dei dati su file JSON
class DatiRepository:
    def __init__(self, path: str,tipo_default=list):
        self.path = path
        self.dati = None
        self.tipo_default = tipo_default
        # se viene caricato un dizionario invece di una lista almeno il programma non crusha. Se viene specificato al riciamo della classe con dict prende dizionario,
        # altrimente rilascia list.
        # questa classe legge il file nei data e lo carica in memoria.
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file) # carica dati in memoria
        # se il file non viene trovato, restituisce una struttura vuota
        except FileNotFoundError:
            print("Errore file non trovato ")
            return self.tipo_default()
            # viene mandato indietro esattamente il tipo di file richiesto
        # se il file è presente ma il formato JSON non è valido
        except json.decoder.JSONDecodeError:
            print("Formato file non valido")
            return self.tipo_default()

    # property che restituisce i dati aggiornati dal file
    @property
    def get_dati(self):
        self.dati = self.read() # manda i dati salvati indietro
        return self.dati

    # salva i dati nel file JSON (sovrascrive il contenuto esistente)
    def salvatggio_dati(self, dati): # self perchè ogni repository è istanziata nel main (sa che file puntare)
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(dati, file, indent=4)
            # json.dump per fissare i dati dalla ram alla memoria
            print("salvataggio effetuato con successo")
        except Exception as e:
            print(f"errore durante il salavataggio {e}")
