
from models.serra import Serra
class GestoreSerra:
    """
    GESTORE SERRA PER IL CONTROLLO DI TUTTE LE SERRE PRESENTI NEL SISTEMA
    """
    def __init__ (self,dati_serra: dict, dati_temperature, dati_umidita, gestore_colture): #ricordati che è listanza del gestore colture nel main se non funziona devi toglierla
        self.dati_temperatura = dati_temperature
        self.dati_umidita = dati_umidita
        self.gestore_colture = gestore_colture
        self.dati_serra = dati_serra
        self.serre_attive={}
        for n_univoco, info_serra in self.dati_serra.items():
            #sistemare sotto il discorso che manda path colture, deve mandare solo dati della serra giusta
            nome_pianta = info_serra["pianta_selezionata"]
            dati_singola_pianta = self.gestore_colture.configurazione_parametri_coltura(nome_pianta)
            serra_attivata=Serra(info_serra["proprietario"],dati_singola_pianta,info_serra["modalita"],self.dati_temperatura, self.dati_umidita,n_univoco, nome_pianta) #attiva una delle serre salvate
            self.serre_attive[n_univoco]=serra_attivata#la mette dentro una lista di serre per mantenerla salvata



    def visualizza_stato_serre(self,n_univoco):
        """
        Metodo per visualizzare dati temperatura,unmidità e stato attuattori
        :param n_univoco:
        :return:
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



    def verifica_esistenza_serra(self, n_univoco):
        """
        Metodo che verifica l'esistenza della serra nel catalogo
        :param n_univoco:
        :return:
        """
        return n_univoco in self.serre_attive


    def aggiungi_serra(self,n_univoco,proprietario):
       """
       Metodo che consente al proprietario di aggiungere una serra al suo parco serre
       :param n_univoco:
       :param proprietario:
       :return:
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
        Metodo con cui il proprietario rimuove una serra dal suo parco serre
        :param n_univoco:
        :param proprietario:
        :return:
        """
        if self.serre_attive[n_univoco].proprietario== proprietario:
            self.serre_attive[n_univoco].proprietario = "nessuno"
            return True, "Serra rimossa con successo"


    def selezione_modalita(self,n_univoco,modalita):
        """
        Metodo che consente al proprietario di selezionare la modalità tra automatica o manuale
        :param n_univoco:
        :param modalita:
        :return:
        """
        if modalita == "automatico":
            self.serre_attive[n_univoco].modalita= modalita
            self.serre_attive[n_univoco].mod_automatica()
            print("modalita modificata, messa automatica")
        elif modalita == "manuale":
            self.serre_attive[n_univoco].modalita = modalita
        #di default disattiva tutti attuatori
            self.serre_attive[n_univoco].mod_manuale_ventole(False)
            self.serre_attive[n_univoco].mod_manuale_sistema_irrigazione(False)
            self.serre_attive[n_univoco].mod_manuale_lampada_UV(False)


    def modifica_coltura_serra(self,n_univoco,pianta):
        """
        Metodo per impostare nella serra le condizioni ideali per la coltura presente
        :param n_univoco:
        :param pianta:
        :return:
        """
        if self.verifica_esistenza_serra(n_univoco):
            pianta_selezionata = self.gestore_colture.configurazione_parametri_coltura(pianta)
            self.serre_attive[n_univoco].set_coltura(pianta_selezionata, pianta)
            return True, "Coltura salvata correttamente"
        else:
            return False, "Errore nel impostare parametri coltura"


    @property
    def dati_salvataggio(self):
        """
        Metodo per sistemare dati da salvare
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
        Metodo per spere la modalità di una serra
        """
        if self.verifica_esistenza_serra(n_univoco):
            mod = self.serre_attive[n_univoco].modalita
            return mod
        else:
            return "nessuna modalita"

    def gestione_manuale_irrigatore(self,n_univoco,stato):
        """
        Metodo per accendere o spegnere irrigatore
        """
        self.serre_attive[n_univoco].mod_manuale_sistema_irrigazione(stato)
        return self.serre_attive[n_univoco].get_stato_sistema_irrigazione

    def gestione_manuale_ventole(self,n_univoco,stato):
        """
        Metodo per accendere o spegnere irrigatore
        """
        self.serre_attive[n_univoco].mod_manuale_ventole(stato)
        return self.serre_attive[n_univoco].get_stato_ventole

    def gestione_manuale_lampadaUV(self,n_univoco,stato):
        """
        Metodo per accendere o spegnere lampadaUV
        """
        self.serre_attive[n_univoco].mod_manuale_lampada_UV(stato)
        return self.serre_attive[n_univoco].get_stato_lampadaUV


    def parco_serre_proprietario(self,proprietario: str):
        """
        Metodo che restituisce le serre univoche a seconda del proprietario
        """
        serre_proprietario = []
        for n_univoco, serra in self.serre_attive.items():#.items(): il ciclo dice per ogni n_univoco ho serre in serre attive, items restituisce la chiave e loggetto serra
            if serra.proprietario == proprietario:
                serre_proprietario.append(n_univoco)
        return serre_proprietario

    def simulazione_aggiornamento_sensori(self):
       """
       Metodo che richiama aggiornamento sensori di tutte le serre
       """
       for serra in self.serre_attive.values():
        serra.aggiornamento_sensori()


    def controllo_periodico(self):
        """
        Controllo periodico delle modalità, se in automatico attiva l'algoritmo di controllo per attivazione attuatori
        """
        for serra in self.serre_attive.values():
            if serra.modalita == "automatico":
                serra.mod_automatica()
