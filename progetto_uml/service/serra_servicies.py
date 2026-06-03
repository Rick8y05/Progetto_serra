from models.serra import Serra

class GestoreSerra:
    def __init__(self, dati_serra: dict, dati_temperature, dati_umidita, gestore_colture):
        self.dati_temperatura = dati_temperature
        self.dati_umidita = dati_umidita
        self.gestore_colture = gestore_colture
        self.dati_serra = dati_serra or {}
        self.serre_attive = {}

        for n_univoco, info_serra in self.dati_serra.items():
            nome_pianta = info_serra.get("pianta_selezionata", "basilico")
            dati_singola_pianta = self.gestore_colture.configurazione_parametri_coltura(nome_pianta)
            serra_attivata = Serra(
                info_serra.get("proprietario", "nessuno"),
                dati_singola_pianta,
                info_serra.get("modalita", "manuale"),
                self.dati_temperatura,
                self.dati_umidita,
                n_univoco,
                nome_pianta,
            )
            self.serre_attive[n_univoco] = serra_attivata

    def get_dati_plancia(self):
        dati_plancia = {}
        for codice, serra in self.serre_attive.items():
            dati_plancia[codice] = {
                "proprietario": serra.proprietario,
                "modalita": serra.modalita,
                "temperatura": serra.get_temperatura_serra,
                "umidita": serra.get_umidita_serra,
                "pianta": serra.nome_pianta,
                "ventole": serra.ventole,
                "irrigazione": serra.irrigazione,
                "lampada_uv": serra.lampada_uv,
            }
        return dati_plancia

    def visualizza_stato_serre(self, n_univoco):
        if not self.verifica_esistenza_serra(n_univoco):
            print(f"Il codice {n_univoco} non esiste ")
            return []

        serra = self.serre_attive[n_univoco]
        return [
            serra.get_umidita_serra,
            serra.get_temperatura_serra,
            serra.get_stato_ventole,
            serra.get_stato_sistema_irrigazione,
            serra.get_stato_lampadaUV,
            serra.modalita,
        ]

    def verifica_esistenza_serra(self, n_univoco):
        return n_univoco in self.serre_attive

    def aggiungi_serra(self, n_univoco, proprietario):
        if self.verifica_esistenza_serra(n_univoco):
            serra = self.serre_attive[n_univoco]
            if serra.proprietario == "nessuno":
                serra.proprietario = proprietario
                return True, "Serra registrata con proprietario corretto"
            return False, "Codice univoco già utilizzato da un altro utente"
        return False, "Numero univoco inesistente"

    def rimuovi_serra(self, n_univoco, proprietario: str):
        if self.verifica_esistenza_serra(n_univoco):
            if self.serre_attive[n_univoco].proprietario == proprietario:
                self.serre_attive[n_univoco].proprietario = "nessuno"
                return True, "Serra rimossa correttamente"
            return False, "Questa serra appartiene ad un altro proprietario"
        return False, "Numero univoco inesistente"

    def set_modalita(self, modalita, n_univoco=None):
        modalita_pulita = str(modalita).strip().lower()

        if n_univoco:
            if not self.verifica_esistenza_serra(n_univoco):
                return False, "Serra non trovata"
            serra = self.serre_attive[n_univoco]
            serra.modalita = modalita_pulita
            if modalita_pulita == "automatica":
                serra.mod_automatica()
            return True, f"Modalità {modalita_pulita} impostata per {n_univoco}"

        for serra in self.serre_attive.values():
            serra.modalita = modalita_pulita
            if modalita_pulita == "automatica":
                serra.mod_automatica()
        return True, f"Modalità {modalita_pulita} impostata per tutte le serre"

    def azione_manuale(self, n_univoco, dispositivo, stato):
        if not self.verifica_esistenza_serra(n_univoco):
            return False, "Serra non trovata"

        serra = self.serre_attive[n_univoco]
        serra.modalita = "manuale"
        stato_bool = str(stato).strip().lower() == "on"
        dispositivo_pulito = str(dispositivo).strip().lower()

        if dispositivo_pulito in ("1", "ventole", "ventole_aereazione"):
            serra.mod_manuale_ventole(stato_bool)
        elif dispositivo_pulito in ("2", "irrigazione", "sistema_irrigazione"):
            serra.mod_manuale_sistema_irrigazione(stato_bool)
        elif dispositivo_pulito in ("3", "lampada_uv", "lampadauv", "lampada uv"):
            serra.mod_manuale_lampada_uv(stato_bool)
        else:
            return False, "Dispositivo non valido"

        return True, "Dispositivo aggiornato"

    def esegui_ciclo_automatico(self):
        for serra in self.serre_attive.values():
            if serra.modalita.lower() == "automatica":
                serra.mod_automatica()
        return True

    def leggi_stato_serra(self, n_univoco):
        return self.serre_attive.get(n_univoco)

    def modifica_coltura_serra(self, n_univoco, pianta):
        if self.verifica_esistenza_serra(n_univoco):
            pianta_selezionata = self.gestore_colture.configurazione_parametri_coltura(pianta)
            self.serre_attive[n_univoco].set_coltura(pianta_selezionata, pianta)
        else:
            print("numero univoco inesistente")

    def elimina_serra(self, n_univoco: str):
        if self.verifica_esistenza_serra(n_univoco):
            self.serre_attive.pop(n_univoco)
        else:
            print("numero univoco inesistente")

    def nuova_serra(self, n_univoco: str, pianta: str = "basilico"):
        if self.verifica_esistenza_serra(n_univoco):
            return False, "Questo codice univoco è già presente"

        dati_coltura = self.gestore_colture.configurazione_parametri_coltura(pianta)
        self.serre_attive[n_univoco] = Serra(
            "nessuno",
            dati_coltura,
            "manuale",
            self.dati_temperatura,
            self.dati_umidita,
            n_univoco,
            pianta,
        )
        return True, "Nuova serra aggiunta"

    @property
    def dati_salvataggio(self):
        dati_salvataggio = {}
        for n_univoco, dati_serra in self.serre_attive.items():
            dati_salvataggio[n_univoco] = {
                "proprietario": dati_serra.proprietario,
                "modalita": dati_serra.modalita,
                "pianta_selezionata": dati_serra.nome_pianta,
            }
        return dati_salvataggio

    def get_modalita(self, n_univoco):
        if self.verifica_esistenza_serra(n_univoco):
            return self.serre_attive[n_univoco].modalita
        print("numero univoco inesistente")
        return "nessuna modalita"

    def gestione_manuale_irrigatore(self, n_univoco, stato):
        if self.verifica_esistenza_serra(n_univoco):
            self.serre_attive[n_univoco].mod_manuale_sistema_irrigazione(stato)
            return self.serre_attive[n_univoco].get_stato_sistema_irrigazione
        return False

    def gestione_manuale_ventole(self, n_univoco, stato):
        if self.verifica_esistenza_serra(n_univoco):
            self.serre_attive[n_univoco].mod_manuale_ventole(stato)
            return self.serre_attive[n_univoco].get_stato_ventole
        return False

    def gestione_manuale_lampadaUV(self, n_univoco, stato):
        if self.verifica_esistenza_serra(n_univoco):
            self.serre_attive[n_univoco].mod_manuale_lampada_uv(stato)
            return self.serre_attive[n_univoco].get_stato_lampadaUV
        return False

    def parco_serre_proprietario(self, proprietario: str):
        serre_proprietario = []
        for n_univoco, serra in self.serre_attive.items():
            if serra.proprietario == proprietario:
                serre_proprietario.append(n_univoco)
        return serre_proprietario
