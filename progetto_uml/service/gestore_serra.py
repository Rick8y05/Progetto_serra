from models.serra import Serra


# classe che gestisce tutte le serre del sistema, sia inserimento/rimozione serra che la logica dell'hardware
class GestoreSerra:
    def __init__ (self,dati_serra: dict, dati_temperature, dati_umidita, gestore_colture): 
		""" INIZIALIZZAZIONE GESTORE SERRA """
        self.dati_temperatura = dati_temperature
        self.dati_umidita = dati_umidita
        self.gestore_colture = gestore_colture
        self.dati_serra = dati_serra
        self.serre_attive={}

		# ciclo di inizializzazione dati dentro il dizionario delle serre attive, per istanziare oggetti
        for n_univoco, info_serra in self.dati_serra.items():
            nome_pianta = info_serra["pianta_selezionata"]
            dati_singola_pianta = self.gestore_colture.configurazione_parametri_coltura(nome_pianta)
            serra_attivata=Serra(info_serra["proprietario"],dati_singola_pianta,info_serra["modalita"],self.dati_temperatura, self.dati_umidita,n_univoco, nome_pianta) #attiva una delle serre salvate
            self.serre_attive[n_univoco]=serra_attivata#la mette dentro una lista di serre per mantenerla salvata
   
	
    def visualizza_stato_serre(self,n_univoco):
		""" 
		Metodo per visualizzare umidità, temperatura e stato attuatori 
		"""
        try:
            umidita = self.serre_attive[n_univoco].get_umidita_serra
            temperatura = self.serre_attive[n_univoco].get_temperatura_serra
            stato_ventole = self.serre_attive[n_univoco].get_stato_ventole
            stato_impianto_irrigazione = self.serre_attive[n_univoco].get_stato_sistema_irrigazione
            stato_lampadaUV = self.serre_attive[n_univoco].get_stato_lampadaUV
            modalita = self.serre_attive[n_univoco].modalita
            return [umidita,temperatura,stato_ventole,stato_impianto_irrigazione,stato_lampadaUV,modalita]
        except KeyError:
            print(f"Il codice {n_univoco} non esiste ")
            return []

	""" metodo che controlla se il codice univoco è presente e quindi esistenza serra """
    def verifica_esistenza_serra(self, n_univoco):
		""" 
		Metodo che controlla se il codice univoco è presente e quindi esistenza serra 
		"""
        return n_univoco in self.serre_attive 
    
  
    def aggiungi_serra(self,n_univoco,proprietario):
		""" 
		Metodo per aggiungere un proprietario ad una serra che non appartiene a nessuno 
		"""
       if self.verifica_esistenza_serra(n_univoco):
            if self.serre_attive[n_univoco].proprietario=="nessuno":
                self.serre_attive[n_univoco].proprietario=proprietario
                return True, "Serra registrata con successo"
            else:
                return False, "Serra appartenente ad un altro utente"
       else:
           return False, "Numero univoco inesistente nel catalogo "
   
   
    def rimuovi_serra(self,n_univoco,proprietario: str):
		""" 
		Metodo rimuove il proprietario da una serra
		"""
                self.serre_attive[n_univoco].proprietario = "nessuno"
                return True, "Serra rimossa con successo"
           
    
    def selezione_modalita(self,n_univoco,modalita):
		 """ 
		 Metodo utilizzato per selezionare modalità (automatica o manuale) 
		 """
        modalita_pulita = modalita.lower()
        if modalita_pulita=="automatico":
            self.serre_attive[n_univoco].modalita= modalita_pulita
            self.serre_attive[n_univoco].mod_automatica()
            print("modalita modificata, messa automatica")
        elif modalita_pulita=="manuale":
            self.serre_attive[n_univoco].modalita = modalita_pulita
        # durante il passagio da automatico a manuale di default disattiva tutti attuatori per sicurezza
            self.serre_attive[n_univoco].mod_manuale_ventole(False)
            self.serre_attive[n_univoco].mod_manuale_sistema_irrigazione(False)
            self.serre_attive[n_univoco].mod_manuale_lampada_UV(False)
            print("modalita modificata, messa manuale")
        else:
            print("modalita non esiste ")

   
    def modifica_coltura_serra(self,n_univoco,pianta):
		""" 
		Modifica la coltura associata a una serra, serve per avere i giusti dati di temperatura e umidità per la modalità automatica 
		"""
        if self.verifica_esistenza_serra(n_univoco):
            pianta_selezionata = self.gestore_colture.configurazione_parametri_coltura(pianta)
            self.serre_attive[n_univoco].set_coltura(pianta_selezionata, pianta)
            return True, "Coltura salvata correttamente"
        else:
            return False, "Errore nel impostare parametri coltura"
   
	
    def elimina_serra(self, n_univoco: str):
		""" 
		Elimina una serra dal catalogo 
		"""
        if self.verifica_esistenza_serra(n_univoco):
            self.serre_attive.pop(n_univoco)
        else:
            print("numero univoco inesistente")
    
	
    def nuova_serra(self, n_univoco: str):
		""" 
		Aggiunge una serra senza dati al catalogo poi i dati vengono inseriti dopo 
		"""
        if self.verifica_esistenza_serra(n_univoco):
            print("questo codice univoco è gia presente")
        else:
            dati = {"proprietario": "nessuno",
                    "modalita": "manuale",
	                "pianta_selezionata": "basilico"
                }
            self.serre_attive[n_univoco] = dati

   
    @property
    def dati_salvataggio(self):
		""" 
		Metodo che prepara i dati per il salvataggio su file 
		"""
        dati_salvataggio = {}
        for n_univoco, dati_serre in self.serre_attive.items():
            dati_salvataggio[n_univoco] = {"proprietario": dati_serre.proprietario,
                    "modalita": dati_serre.modalita,
	                "pianta_selezionata": dati_serre.nome_pianta
                }
        return dati_salvataggio

    
    def get_modalita(self, n_univoco):
		""" 
		Metodo che restituisce la modalità di una serra
		"""
        if self.verifica_esistenza_serra(n_univoco):
            mod = self.serre_attive[n_univoco].modalita
            return mod
        else:
            print("numero univoco inesistente")
            return "nessuna modalita"

    
    def gestione_manuale_irrigatore(self,n_univoco,stato):
		 """ 
		 Controllo manuale irrigazione 
		 """
        self.serre_attive[n_univoco].mod_manuale_sistema_irrigazione(stato)
        return self.serre_attive[n_univoco].get_stato_sistema_irrigazione

  
    def gestione_manuale_ventole(self,n_univoco,stato):
		 """ 
		 Controllo manuale ventole 
		 """
        self.serre_attive[n_univoco].mod_manuale_ventole(stato)
        return self.serre_attive[n_univoco].get_stato_ventole

   
    def gestione_manuale_lampadaUV(self,n_univoco,stato):
		""" 
		Controllo manuale lampada UV 
		"""
        self.serre_attive[n_univoco].mod_manuale_lampada_UV(stato)
        return self.serre_attive[n_univoco].get_stato_lampadaUV


    def parco_serre_proprietario(self,proprietario: str):
	""" 
	Metodo per definire le serre che ha a disposizione il proprietario, quindi solamente 
	quelle che puo usare, senza correrere il rischio che gestisca anche serre non sue 
	"""
        serre_proprietario = []
        for n_univoco, serra in self.serre_attive.items():  # .items(): il ciclo dice per ogni n_univoco ho serre in serre attive, items restituisce la chiave e l'oggetto serra
            if serra.proprietario == proprietario:
                serre_proprietario.append(n_univoco)
        return serre_proprietario


    def simulazione_aggiornamento_sensori(self):
		""" 
		Metodo che chiama per ogni serra l'aggiornamento sensori 
		"""
       for serra in self.serre_attive.values():
        serra.aggiornamento_sensori()
		   
	
    def controllo_periodico(self):
		""" 
		Controllo periodico, se la serra è in automatico attiva l'algoritmo che regola gli attuatori in base alle temperature 
		"""
        for serra in self.serre_attive.values():
            if serra.modalita == "automatico":
                serra.mod_automatica()
