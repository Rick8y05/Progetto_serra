def main():
    from repository.lettore_dati import DatiRepository
    from service.gestore_colture import GestoreColture
    from service.gestore_serra import GestoreSerra
    from GUI.menu_principale import InterfacciaMacOS
    from service.gestore_tempo import GestoreTempo
    from GUI.schermata_aggiungi_serra import SchermataAggiungiSerra
    from GUI.schermata_rimuovi_serra import SchermataRimuoviSerra
    from GUI.schermata_configura_parametri_coltura import SchermataConfiguraParametriColtura
    from GUI.schermata_caricare_dati_coltura import SchermataCaricareDatiColtura
    from GUI.schermata_visualizza_dati_serra import VisualizzaDatiSerra
    from GUI.schermata_azzionamento_attuatori import AzionamentoAttuatori
    from GUI.schermata_seleziona_modalita_funzionamento import SelezionaModalitaFunzionamento
    from GUI.schermata_menu_operatore import MenuOperatore
    from GUI.schermata_visualizza_dati_serra_operatore import VisualizzaDatiSerraOperatore
    from GUI.schermata_aggiornamento_parametri import AggiornaParametriColtureOperatore
    from service.autenticazione import Autenticazione
    from GUI.menu_autenticazione import SchermataLogin
    from GUI.menu_registrazione import SchermataRegistrazione
    import sys
    from PyQt6.QtWidgets import QApplication,QStackedWidget
    
    # path dei file JSON
    path_cat_serre="data/catalogo_serre.json"
    path_colture="data/colture.json"
    path_dati_colt_utente="data/dati_colture_utente.json"
    path_val_temperatura = "data/valori_temperature.json"
    path_val_umidita = "data/valori_umidita.json"
    path_utenti = "data/utenti.json"
    
    # repository
    repository_serre = DatiRepository(path_cat_serre)
    repository_colture = DatiRepository(path_colture)
    repository_dati_colt_utente = DatiRepository(path_dati_colt_utente)
    repository_val_temperatura = DatiRepository(path_val_temperatura)
    repository_val_umidita = DatiRepository(path_val_umidita)
    repository_utenti = DatiRepository(path_utenti)
    

    gestore_colture = GestoreColture(repository_colture.get_dati,repository_dati_colt_utente.get_dati)
    gestore_serra = GestoreSerra(repository_serre.get_dati,repository_val_temperatura.get_dati,repository_val_umidita.get_dati, gestore_colture)
    gestore_tempo = GestoreTempo(gestore_serra,10)
    gestore_autenticazione = Autenticazione(repository_utenti.get_dati)
    

    gestore_tempo.avvia()
    

    app = QApplication(sys.argv)
    proiettore_pagine = QStackedWidget()
    proiettore_pagine.setStyleSheet("""
        QStackedWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 #2C3E50, 
                                        stop:0.5 #0F2027, 
                                        stop:1 #203A43);
        }
        QWidget {
            font-family: '.AppleSystemUIFont', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
        }
    """)


    menu_principale_proprietario = InterfacciaMacOS(gestore_serra,gestore_colture,gestore_tempo,proiettore_pagine)
    schermata_aggiungi_serra = SchermataAggiungiSerra(proiettore_pagine, gestore_serra)
    schermata_rimuovi_serra = SchermataRimuoviSerra(proiettore_pagine, gestore_serra)
    schermata_configura_parametri_coltura = SchermataConfiguraParametriColtura(proiettore_pagine, gestore_serra, gestore_colture)
    schermata_caricare_dati_coltura = SchermataCaricareDatiColtura(proiettore_pagine, gestore_serra, gestore_colture)
    schermata_visualizza_dati_serra = VisualizzaDatiSerra(proiettore_pagine, gestore_serra, gestore_colture)
    schermata_azionamento_attuatori = AzionamentoAttuatori(proiettore_pagine, gestore_serra, gestore_colture)
    schermata_seleziona_modalita_funzionamento= SelezionaModalitaFunzionamento(proiettore_pagine, gestore_serra, gestore_colture)
    schermata_menu_operatore = MenuOperatore(gestore_serra, gestore_colture, gestore_tempo,proiettore_pagine)
    schermata_visualizza_dati_serra_operatore =  VisualizzaDatiSerraOperatore(proiettore_pagine, gestore_serra, gestore_colture )
    schermata_aggiorna_parametri_colture = AggiornaParametriColtureOperatore(proiettore_pagine, gestore_serra, gestore_colture)
    schermata_login = SchermataLogin(proiettore_pagine,gestore_autenticazione)
    schermata_registrazione = SchermataRegistrazione(proiettore_pagine,gestore_autenticazione)
    
    # registrazione schermate nel proiettore
    proiettore_pagine.addWidget(menu_principale_proprietario)   # Indice 0
    proiettore_pagine.addWidget(schermata_aggiungi_serra) #1
    proiettore_pagine.addWidget(schermata_rimuovi_serra) #2
    proiettore_pagine.addWidget(schermata_configura_parametri_coltura) #3
    proiettore_pagine.addWidget(schermata_caricare_dati_coltura) #4
    proiettore_pagine.addWidget(schermata_visualizza_dati_serra) #5
    proiettore_pagine.addWidget(schermata_azionamento_attuatori) #6
    proiettore_pagine.addWidget(schermata_seleziona_modalita_funzionamento) #7
    proiettore_pagine.addWidget(schermata_menu_operatore) #8
    proiettore_pagine.addWidget(schermata_visualizza_dati_serra_operatore) #9
    proiettore_pagine.addWidget(schermata_aggiorna_parametri_colture) #10
    proiettore_pagine.addWidget(schermata_login) #11
    proiettore_pagine.addWidget(schermata_registrazione) #12
    
    # schermata iniziale
    proiettore_pagine.setCurrentIndex(11)
    #apertura dell'interfaccia a schermo intero 
    proiettore_pagine.showFullScreen() 
     # ciclo loop infinito per lasciare in attesa l'interfaccia della richiesta dell'utente
    status = app.exec() 
    
    # salvataggio dati 
    repository_serre.salvataggio_dati(gestore_serra.dati_salvataggio)
    repository_dati_colt_utente.salvataggio_dati(gestore_colture.dati_colture_utente)
    repository_colture.salvataggio_dati(gestore_colture.dati_colture)
    repository_utenti.salvataggio_dati(gestore_autenticazione.repo)
    # termine simulazione sensori
    gestore_tempo.ferma()
    
    sys.exit(status)
    
if __name__ == "__main__":
    main()


