from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

# selezione della modalità di funzionamento
class SelezionaModalitaFunzionamento(QWidget):
    def __init__(self, proiettore_pagine, gestore_serra, gestore_colture):
        super().__init__()
        self.proprietario = ""
        self.proiettore_pagine = proiettore_pagine
        self.gestore_serra = gestore_serra
        self.gestore_colture = gestore_colture
        self.contenitore_dashboard = None
        self.serra_corrente_attiva = None
        self.modalita_selezionata = None
        self.inizializza_interfaccia()

    def inizializza_interfaccia(self):
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                font-family: '.AppleSystemUIFont', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                color: #FFFFFF;
            }
        """)

        layout_principale = QVBoxLayout()
        layout_principale.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_centrale = QFrame()
        card_centrale.setFixedWidth(850)
        card_centrale.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
            }
        """)

        self.layout_card = QVBoxLayout(card_centrale)
        self.layout_card.setContentsMargins(50, 50, 50, 50)
        self.layout_card.setSpacing(20)

        # titolo
        titolo = QLabel("MODALITÀ FUNZIONAMENTO")
        titolo.setStyleSheet("""
            QLabel {
                font-size: 36px; 
                font-weight: 700; 
                letter-spacing: -0.5px;
                color: #FFFFFF;
                border: none;
                background: transparent;
            }
        """)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_card.addWidget(titolo)

        # sottotitolo
        self.sottotitolo = QLabel("Seleziona la serra su cui desideri operare")
        self.sottotitolo.setStyleSheet(
            "font-size: 18px; color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
        self.sottotitolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_card.addWidget(self.sottotitolo)

        self.layout_card.addSpacing(10)

        self.layout_bottoni_serre = QHBoxLayout()
        self.layout_bottoni_serre.setSpacing(15)
        self.layout_card.addLayout(self.layout_bottoni_serre)

        self.label_messaggio = QLabel("")
        self.label_messaggio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_messaggio.setStyleSheet("font-size: 14px; font-weight: 500; border: none; background: transparent;")
        self.layout_card.addWidget(self.label_messaggio)
        self.layout_card.addSpacing(10)

        # bottoni in basso
        layout_comandi_bassi = QHBoxLayout()
        layout_comandi_bassi.setSpacing(15)

        # bottone annulla e torna al menu
        self.btn_annulla = QPushButton("Annulla e torna al Menù")
        self.btn_annulla.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_annulla.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.7);
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); color: #FFFFFF; }
        """)
        self.btn_annulla.clicked.connect(self.torna_al_menu)

        # bottone per salvare la modalità selezionata
        self.btn_salva = QPushButton("Salva Modalità")
        self.btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_salva.setEnabled(False)  # Disabilitato finché non si seleziona una serra
        self.btn_salva.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 700;
                color: #FFFFFF;
            }
            QPushButton:hover { background-color: #1B5E20; }
            QPushButton:disabled { background-color: rgba(255, 255, 255, 0.02); color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.05); }
        """)
        self.btn_salva.clicked.connect(self.salva_modalita)

        layout_comandi_bassi.addStretch(1)
        layout_comandi_bassi.addWidget(self.btn_annulla)
        layout_comandi_bassi.addWidget(self.btn_salva)
        layout_comandi_bassi.addStretch(1)

        self.layout_card.addLayout(layout_comandi_bassi)

        layout_principale.addWidget(card_centrale)
        self.setLayout(layout_principale)

        self.aggiorna_pulsanti_serre()

    def aggiorna_pulsanti_serre(self):
        self.svuota_layout_bottoni()
        self.btn_salva.setEnabled(False)
        n_univoci_proprietario = self.gestore_serra.parco_serre_proprietario(self.proprietario)

        # mancanza di serre registrate nel profilo
        if not n_univoci_proprietario:
            label_vuota = QLabel("Non hai nessuna serra registrata nel tuo profilo.")
            label_vuota.setStyleSheet(
                "font-size: 14px; color: rgba(255, 255, 255, 0.4); font-style: italic; border: none; background: transparent;")
            self.layout_bottoni_serre.addWidget(label_vuota, alignment=Qt.AlignmentFlag.AlignCenter)
            return

        self.layout_bottoni_serre.addStretch(1)

        for n_univoco in n_univoci_proprietario:
            btn_serra = QPushButton(f"SERRA \n{n_univoco}")
            btn_serra.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_serra.setFixedSize(140, 90)
            btn_serra.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.06);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 16px;
                    font-size: 14px;
                    font-weight: 600;
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: rgba(30, 136, 229, 0.15);
                    border-color: #1E88E5;
                }
            """)
            btn_serra.clicked.connect(
                lambda checked, id_scelto=n_univoco: self.schermata_seleziona_stato_attuatori(id_scelto))
            self.layout_bottoni_serre.addWidget(btn_serra)

        self.layout_bottoni_serre.addStretch(1)

    # selezione stato attuatori
    def schermata_seleziona_stato_attuatori(self, n_univoco):
        self.svuota_layout_bottoni()
        self.serra_corrente_attiva = n_univoco
        self.btn_salva.setEnabled(True)

        if self.modalita_selezionata is None:
            self.modalita_selezionata = str(self.gestore_serra.get_modalita(n_univoco)).lower()

        self.sottotitolo.setText(f"Imposta funzionamento - SERRA {n_univoco}")

        self.contenitore_dashboard = QWidget()
        dashboard_layout = QVBoxLayout(self.contenitore_dashboard)
        dashboard_layout.setSpacing(20)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)

        layout_scelta = QHBoxLayout()
        layout_scelta.setSpacing(20)

        # bottone modalità manuale
        self.btn_manuale = QPushButton("MANUALE")
        self.btn_manuale.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_manuale.setFixedSize(180, 60)

        # bottone modalità automatica
        self.btn_automatica = QPushButton("AUTOMATICA")
        self.btn_automatica.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_automatica.setFixedSize(180, 60)

        self.aggiorna_grafica_pulsanti_modalita()

        self.btn_manuale.clicked.connect(lambda: self.cambia_selezione_locale("manuale"))
        self.btn_automatica.clicked.connect(lambda: self.cambia_selezione_locale("automatico"))

        layout_scelta.addStretch(1)
        layout_scelta.addWidget(self.btn_manuale)
        layout_scelta.addWidget(self.btn_automatica)
        layout_scelta.addStretch(1)

        dashboard_layout.addLayout(layout_scelta)

        # bottone intermedio per tornare indietro alle serre annullando le modifiche non salvate
        btn_indietro = QPushButton("Seleziona un'altra Serra")
        btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_indietro.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.6);
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); color: #FFFFFF; }
        """)
        btn_indietro.clicked.connect(self.ripristina_schermata_selezione)
        dashboard_layout.addWidget(btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout_bottoni_serre.addWidget(self.contenitore_dashboard)

    def cambia_selezione_locale(self, mod):
        self.modalita_selezionata = mod
        self.aggiorna_grafica_pulsanti_modalita()

    def aggiorna_grafica_pulsanti_modalita(self):
        if 'manual' in self.modalita_selezionata:
            self.btn_manuale.setStyleSheet("""
                QPushButton { background-color: #1E88E5; border: 2px solid #1E88E5; border-radius: 14px; font-size: 14px; font-weight: 700; color: #FFFFFF; }
            """)
            self.btn_automatica.setStyleSheet("""
                QPushButton { background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.6); }
                QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); color: #FFFFFF; }
            """)
        else:
            self.btn_manuale.setStyleSheet("""
                QPushButton { background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.6); }
                QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); color: #FFFFFF; }
            """)
            self.btn_automatica.setStyleSheet("""
                QPushButton { background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 14px; font-size: 14px; font-weight: 700; color: #FFFFFF; }
            """)

    def salva_modalita(self):
        if self.serra_corrente_attiva and self.modalita_selezionata:
            self.gestore_serra.selezione_modalita(self.serra_corrente_attiva, self.modalita_selezionata)
            self.label_messaggio.setText("")

            self.ripristina_schermata_selezione()
            self.proiettore_pagine.setCurrentIndex(0)

    def ripristina_schermata_selezione(self):
        self.modalita_selezionata = None
        self.serra_corrente_attiva = None
        self.btn_salva.setEnabled(False)

        if self.contenitore_dashboard is not None:
            self.layout_bottoni_serre.removeWidget(self.contenitore_dashboard)
            self.contenitore_dashboard.setParent(None)
            self.contenitore_dashboard.deleteLater()
            self.contenitore_dashboard = None

        self.sottotitolo.setText("Seleziona la serra su cui desideri operare")
        self.aggiorna_pulsanti_serre()

    def svuota_layout_bottoni(self):
        if self.layout_bottoni_serre is not None:
            while self.layout_bottoni_serre.count():
                item = self.layout_bottoni_serre.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    del item

    def torna_al_menu(self):
        if hasattr(self, 'label_messaggio') and self.label_messaggio:
            self.label_messaggio.setText("")
        self.ripristina_schermata_selezione()
        self.proiettore_pagine.setCurrentIndex(0)

    def showEvent(self, event):
        super().showEvent(event)

        if self.proiettore_pagine.utente_corrente is not None:
            utente = self.proiettore_pagine.utente_corrente
            self.proprietario = getattr(utente, 'full_name', None) or getattr(utente, 'nome', None) or (utente[0] if isinstance(utente, (list, tuple)) and len(utente) > 0 else str(utente))

        if hasattr(self, 'label_messaggio') and self.label_messaggio:
            self.label_messaggio.setText("")

        self.ripristina_schermata_selezione()
