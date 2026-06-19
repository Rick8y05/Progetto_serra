from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer


class AzionamentoAttuatori(QWidget):
    def __init__(self, proiettore_pagine, gestore_serra, gestore_colture):
        super().__init__()
        self.proiettore_pagine = proiettore_pagine
        self.gestore_serra = gestore_serra
        self.gestore_colture = gestore_colture

        self.proprietario = ""
        self.contenitore_dashboard = None
        self.serra_corrente_attiva = None

        # Dizionario per memorizzare lo stato dei comandi prima del salvataggio effettivo
        self.stati_temporanei = {"ventole": False, "irrigatore": False, "lampada": False}

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

        titolo = QLabel("AZIONAMENTO ATTUATORI")
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

        self.sottotitolo = QLabel("Seleziona la serra su cui desideri operare")
        self.sottotitolo.setStyleSheet("font-size: 18px; color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
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

        layout_comandi_bassi = QHBoxLayout()
        layout_comandi_bassi.setSpacing(15)

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

        self.btn_salva = QPushButton("Salva Impostazioni")
        self.btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_salva.setVisible(False)
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
        """)
        self.btn_salva.clicked.connect(self.salva_impostazioni)

        layout_comandi_bassi.addStretch(1)
        layout_comandi_bassi.addWidget(self.btn_annulla)
        layout_comandi_bassi.addWidget(self.btn_salva)
        layout_comandi_bassi.addStretch(1)

        self.layout_card.addLayout(layout_comandi_bassi)

        layout_principale.addWidget(card_centrale)
        self.setLayout(layout_principale)

    def aggiorna_pulsanti_serre(self):
        self.svuota_layout_bottoni()
        self.btn_salva.setVisible(False)
        n_univoci_proprietario = self.gestore_serra.parco_serre_proprietario(self.proprietario)

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

    def schermata_seleziona_stato_attuatori(self, n_univoco):
        # recuepro modalità 
        mod = self.gestore_serra.get_modalita(n_univoco)

        # controllo stringa: se "automatica", blocca l'azione e mostra l'errore in rosso senza rompere la griglia
        if self.gestore_serra.serre_attive[n_univoco].modalita in ["automatico"]:
            self.label_messaggio.setStyleSheet(
                "font-size: 14px; font-weight: 600; color: #FF3B30; border: none; background: transparent;")
            self.label_messaggio.setText(
                f"✕ Errore: la SERRA {n_univoco} è in modalità Automatica! Vai in 'Selezione Modalità Funzionamento' per cambiarla.")
            return

        # solo se è in "manuale" procediamo a svuotare e mostrare il pannello di controllo
        self.label_messaggio.setText("")
        self.svuota_layout_bottoni()
        self.serra_corrente_attiva = n_univoco
        self.btn_salva.setVisible(True)

        self.sottotitolo.setText(f"Pannello di Controllo - SERRA {n_univoco}")

        self.contenitore_dashboard = QWidget()
        dashboard_layout = QVBoxLayout(self.contenitore_dashboard)
        dashboard_layout.setSpacing(15)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)

        dati_attuali = self.gestore_serra.visualizza_stato_serre(n_univoco)
        self.stati_temporanei["ventole"] = dati_attuali[2] if dati_attuali else False
        self.stati_temporanei["irrigatore"] = dati_attuali[3] if dati_attuali else False
        self.stati_temporanei["lampada"] = dati_attuali[4] if dati_attuali else False

        card_comandi = QFrame()
        card_comandi.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px;")
        lyt_comandi = QVBoxLayout(card_comandi)
        lyt_comandi.setContentsMargins(20, 20, 20, 20)
        lyt_comandi.setSpacing(15)

        def crea_riga_interruttore(nome, chiave_stato):
            riga = QHBoxLayout()
            lbl = QLabel(nome)
            lbl.setStyleSheet("font-size: 15px; font-weight: 500; border: none;")

            btn = QPushButton()
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(100, 35)

            def imposta_stile_tasto(attivo):
                if attivo:
                    btn.setText("ON")
                    btn.setStyleSheet("background-color: #4CAF50; border: none; border-radius: 8px; font-weight: 700; color: white;")
                else:
                    btn.setText("OFF")
                    btn.setStyleSheet("background-color: #555555; border: none; border-radius: 8px; font-weight: 700; color: rgba(255,255,255,0.6);")

            imposta_stile_tasto(self.stati_temporanei[chiave_stato])

            def al_click():
                nuovo_stato = not self.stati_temporanei[chiave_stato]
                self.stati_temporanei[chiave_stato] = nuovo_stato if 'Admin_nuovo_stato' in locals() else nuovo_stato
                self.stati_temporanei[chiave_stato] = nuovo_stato
                imposta_stile_tasto(nuovo_stato)

            btn.clicked.connect(al_click)
            riga.addWidget(lbl)
            riga.addStretch()
            riga.addWidget(btn)
            return riga

        lyt_comandi.addLayout(crea_riga_interruttore("ventole:", "ventole"))
        lyt_comandi.addLayout(crea_riga_interruttore("irrigatore:", "irrigatore"))
        lyt_comandi.addLayout(crea_riga_interruttore("lampada uv:", "lampada"))

        dashboard_layout.addWidget(card_comandi)

        btn_indietro = QPushButton("Seleziona un'altra Serra")
        btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_indietro.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.7);
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); color: #FFFFFF; }
        """)
        btn_indietro.clicked.connect(self.ripristina_schermata_selezione)
        dashboard_layout.addWidget(btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout_bottoni_serre.addWidget(self.contenitore_dashboard)

    def salva_impostazioni(self):
        if self.serra_corrente_attiva:
            self.gestore_serra.gestione_manuale_ventole(self.serra_corrente_attiva, self.stati_temporanei["ventole"])
            self.gestore_serra.gestione_manuale_irrigatore(self.serra_corrente_attiva,
                                                           self.stati_temporanei["irrigatore"])
            self.gestore_serra.gestione_manuale_lampadaUV(self.serra_corrente_attiva, self.stati_temporanei["lampada"])

            self.ripristina_schermata_selezione()
            self.proiettore_pagine.setCurrentIndex(0)

    def ripristina_schermata_selezione(self):
        self.serra_corrente_attiva = None
        self.btn_salva.setVisible(False)

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
                del item

    def torna_al_menu(self):
        self.label_messaggio.setText("")
        self.ripristina_schermata_selezione()
        self.proiettore_pagine.setCurrentIndex(0)

    def showEvent(self, event):
        super().showEvent(event)
        if self.proiettore_pagine.utente_corrente is not None:
            utente = self.proiettore_pagine.utente_corrente
            self.proprietario = getattr(utente, 'full_name', None) or getattr(utente, 'nome', None) or (utente[0] if isinstance(utente, (list, tuple)) and len(utente) > 0 else str(utente))

        self.label_messaggio.setText("")
        QTimer.singleShot(50, self.ripristina_schermata_selezione)
