from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,QApplication
from PyQt6.QtCore import Qt, QTimer

# schermata principale del sistema
class InterfacciaMacOS(QWidget):
    def __init__(self, gestore_serra, gestore_colture, gestore_tempo,proiettore_pagine):
        super().__init__()
        self.gestore_serra = gestore_serra
        self.gestore_colture = gestore_colture
        self.gestore_tempo = gestore_tempo
        self.nome_proprietario = ""
        self.proiettore_pagine = proiettore_pagine
        # titolo finestra
        self.setWindowTitle("Pannello di Controllo Serra")
        #self.resize(650, 450)  # Stile box Apple trovato su internet

        # Inizializziamo la grafica pulita
        self.finestra_principale()

    # costruzione interfaccia principale
    def finestra_principale(self):
        # stile generale schermata
        self.setStyleSheet("""
            QWidget {
                font-family: '.AppleSystemUIFont', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
            }
        """) # font del testo della apple

        # layout verticale
        layout_principale = QVBoxLayout()
        layout_principale.setContentsMargins(50, 60, 50, 60) # margini
        layout_principale.setSpacing(0) # spazio tra i bordi rimosso

        # sfondo trasparente
        self.setObjectName("FinestraPrincipale")
        self.setStyleSheet("""
                     QWidget#FinestraPrincipale {
                         background: transparent;
                     }""")
    
        # messaggio di benvenuto
        testo_benvenuto = QLabel(f"Benvenuto {self.nome_proprietario}")
        testo_benvenuto.setStyleSheet("font-size: 32px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.5px;") # caratteri
        testo_benvenuto.setAlignment(Qt.AlignmentFlag.AlignCenter) # allinea al centro il titolo

        sottotitolo = QLabel("Pannello di controllo software della serra automatizzata")
        sottotitolo.setStyleSheet("font-size: 14px; color: #B0C4DE; font-weight: 400; margin-top: 8px;")
        sottotitolo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_principale.addWidget(testo_benvenuto)
        layout_principale.addWidget(sottotitolo)

        layout_principale.addSpacing(50)

        # contenitore pulsanti effetto vetro, modello online
        pannello_comandi = QWidget()
        pannello_comandi.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 16px;
            }
        """)

        layout_bottoni = QVBoxLayout(pannello_comandi)
        layout_bottoni.setContentsMargins(25, 25, 25, 25)
        layout_bottoni.setSpacing(14)

        btn_aggiungi_serra = QPushButton("Aggiungi Serra")
        btn_aggiungi_serra.clicked.connect(lambda: self.proiettore_pagine.setCurrentIndex(1)) # lambda serve a dire al python "non eseguire subito, ma metti la funzione "proiettore" in una funzione chiusa temporanea e aspetta che il bottone venga cliccato"
        btn_rimuovi_serra = QPushButton("Rimuovi Serra")
        btn_rimuovi_serra.clicked.connect(lambda: self.proiettore_pagine.setCurrentIndex(2))
        btn_configura_parametri_coltura = QPushButton("Configura Parametri Coltura")
        btn_configura_parametri_coltura.clicked.connect(lambda: self.proiettore_pagine.setCurrentIndex(3))
        btn_caricare_dati_coltura = QPushButton("Caricare Dati Coltura")
        btn_caricare_dati_coltura.clicked.connect(lambda: self.proiettore_pagine.setCurrentIndex(4))
        btn_visualizza_dati_serra = QPushButton("Visualizza Dati Serra")
        btn_visualizza_dati_serra.clicked.connect(lambda: self.proiettore_pagine.setCurrentIndex(5))
        btn_azionamento_disp = QPushButton("Azionamento Attuatori")
        btn_azionamento_disp.clicked.connect(lambda: self.proiettore_pagine.setCurrentIndex(6))
        btn_seleziona_mod = QPushButton("Selezione Modalità Funzionamento")
        btn_seleziona_mod.clicked.connect(lambda: self.proiettore_pagine.setCurrentIndex(7))
        btn_exit = QPushButton("Esci")
        btn_exit.clicked.connect(QApplication.quit)

        # stile unico per bottoni
        stile_mac_premium = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 500;
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 14px 28px;
                min-width: 280px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.05);
            }
        """
        # assegnazione stile ai bottoni
        btn_aggiungi_serra.setStyleSheet(stile_mac_premium)
        btn_rimuovi_serra.setStyleSheet(stile_mac_premium)
        btn_configura_parametri_coltura.setStyleSheet(stile_mac_premium)
        btn_caricare_dati_coltura.setStyleSheet(stile_mac_premium)
        btn_visualizza_dati_serra.setStyleSheet(stile_mac_premium)
        btn_azionamento_disp.setStyleSheet(stile_mac_premium)
        btn_seleziona_mod.setStyleSheet(stile_mac_premium)
        btn_exit.setStyleSheet(stile_mac_premium)
        
        # gestione logica bottoni
        btn_aggiungi_serra.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_rimuovi_serra.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_seleziona_mod.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_visualizza_dati_serra.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_azionamento_disp.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_caricare_dati_coltura.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_configura_parametri_coltura.setCursor(Qt.CursorShape.PointingHandCursor)


        layout_bottoni.addWidget(btn_aggiungi_serra, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_bottoni.addWidget(btn_rimuovi_serra, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_bottoni.addWidget(btn_configura_parametri_coltura, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_bottoni.addWidget(btn_caricare_dati_coltura, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_bottoni.addWidget(btn_visualizza_dati_serra, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_bottoni.addWidget(btn_azionamento_disp, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_bottoni.addWidget(btn_seleziona_mod, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_bottoni.addWidget(btn_exit, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_principale.addWidget(pannello_comandi, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principale.addStretch(1)

        self.setLayout(layout_principale)

    def showEvent(self, event):
        super().showEvent(event)

        if self.proiettore_pagine.utente_corrente is not None:
            utente = self.proiettore_pagine.utente_corrente
            self.nome_proprietario = (
                utente.nome if hasattr(utente, 'nome') else utente[0]
            )
