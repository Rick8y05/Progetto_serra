import json
class DatiRepository:
    def __init__(self, path: str, tipo_default=list):
        self.path = path
        self.dati = None
        self.tipo_default = tipo_default #questa cosa serve perchè se viene caricata un
        #dizionario invece di una lista almeno il programma non esplode e cosa fa, se viene
        #specificato al riciamo della classe con dict prende dizionario altrimente rilascia list
    #questa classe sotto legge il file nei data e lo carica in memoria
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)#carica dati in memoria
        except FileNotFoundError:
            print("Errore file non trovato ")
            return self.tipo_default()#cosi rimandiamo indietro esattamente il tipo di file richiesto
        except json.decoder.JSONDecodeError:
            print("Formato file non valido")
            return self.tipo_default()
    @property
    def get_dati(self):
        self.dati = self.read() #manda i dati salvati indietro
        return self.dati

    # salvataggio dati nel file json
    def save(self, dati):
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(dati, file, indent=4, ensure_ascii=False)
        except IOError:
            print("Errore nel salvataggio del file")
