from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit
from PyQt6.QtCore import Qt, QTimer


class SchermataCaricareDatiColtura(QWidget):
    def __init__(self, proiettore_pagine, gestore_serra, gestore_coltura):
        super().__init__()
        self.proiettore_pagine = proiettore_pagine
        self.gestore_serra = gestore_serra
        self.proprietario = ""
        self.gestore_coltura = gestore_coltura

        # Variabili di stato
        self.pianta_corrente = ""
        self.fabbrica_corrente = False

        self.layout_bottoni_colture = None
        self.label_messaggio = None
        self.busto = None
        self.altezza = None

        # Definiamo un layout principale fisso per l'intero Widget di base
        self.layout_principale_schermata = QVBoxLayout(self)
        self.layout_principale_schermata.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selezione_coltura()

    def svuota_schermata(self):
        # Pulisce in sicurezza il layout principale senza distruggerlo.
        layout = self.layout_principale_schermata
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.hide()
                    widget.setParent(None)
                    widget.deleteLater()
                # Se c'è un sotto-layout, lo puliamo
                elif item.layout() is not None:
                    self.svuota_sub_layout(item.layout())

    def svuota_sub_layout(self, layout):
        """Metodo ricorsivo per pulire i sotto-layout interni ed evitare leak di memoria."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout() is not None:
                self.svuota_sub_layout(item.layout())
            del item

    def svuota_layout_bottoni(self):
        """Svuota specificamente il contenitore dei pulsanti orizzontali delle colture."""
        if self.layout_bottoni_colture is not None:
            while self.layout_bottoni_colture.count():
                item = self.layout_bottoni_colture.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                del item

    def selezione_coltura(self):
        self.svuota_schermata()

        self.setStyleSheet("""
                            QWidget {
                                background-color: transparent;
                                font-family: '.AppleSystemUIFont', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                                color: #FFFFFF;
                            }
                        """)

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

        titolo = QLabel("CARICARE DATI COLTURA")
        titolo.setStyleSheet(
            "font-size: 36px; font-weight: 700; letter-spacing: -0.5px; color: #FFFFFF; border: none; background: transparent;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_card.addWidget(titolo)

        self.sottotitolo = QLabel("Seleziona la coltura presente nella tua serra")
        self.sottotitolo.setStyleSheet("font-size: 18px; color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
        self.sottotitolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_card.addWidget(self.sottotitolo)

        self.layout_card.addSpacing(10)

        self.layout_bottoni_colture = QHBoxLayout()
        self.layout_bottoni_colture.setSpacing(15)
        self.layout_card.addLayout(self.layout_bottoni_colture)

        self.label_messaggio = QLabel("")
        self.label_messaggio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_messaggio.setStyleSheet("font-size: 14px; font-weight: 500; border: none; background: transparent;")
        self.layout_card.addWidget(self.label_messaggio)
        self.layout_card.addSpacing(10)

        btn_annulla = QPushButton("Annulla e torna al Menù")
        btn_annulla.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_annulla.setStyleSheet("""
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
        btn_annulla.clicked.connect(self.torna_al_menu)
        self.layout_card.addWidget(btn_annulla, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout_principale_schermata.addWidget(card_centrale)

        # recupero colture disponibili
        colture_disponibili = self.gestore_coltura.colture_disponibili()

        if not colture_disponibili:
            label_vuota = QLabel("Al momento non sono presenti colture da selezionare")
            label_vuota.setStyleSheet(
                "font-size: 14px; color: rgba(255, 255, 255, 0.4); font-style: italic; border: none; background: transparent;")
            self.layout_bottoni_colture.addWidget(label_vuota, alignment=Qt.AlignmentFlag.AlignCenter)
            return

        self.layout_bottoni_colture.addStretch(1)

        for pianta in colture_disponibili:
            btn_colture = QPushButton(f"{pianta}")
            btn_colture.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_colture.setFixedSize(140, 90)
            btn_colture.setStyleSheet("""
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
            btn_colture.clicked.connect(lambda checked, p=pianta: self.selezione_tipo_impostazioni(p))
            self.layout_bottoni_colture.addWidget(btn_colture)

        self.layout_bottoni_colture.addStretch(1)

    def selezione_tipo_impostazioni(self, pianta):
        self.svuota_schermata()

        self.setStyleSheet("""
                            QWidget {
                                background-color: transparent;
                                font-family: '.AppleSystemUIFont', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                                color: #FFFFFF;
                            }
                        """)

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

        titolo = QLabel("CARICARE DATI COLTURA")
        titolo.setStyleSheet(
            "font-size: 36px; font-weight: 700; letter-spacing: -0.5px; color: #FFFFFF; border: none; background: transparent;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_card.addWidget(titolo)

        self.sottotitolo = QLabel("Seleziona il tipo di impostazioni che hai usato per la tua coltura")
        self.sottotitolo.setStyleSheet(
            "font-size: 18px; color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
        self.sottotitolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_card.addWidget(self.sottotitolo)

        self.layout_card.addSpacing(10)

        self.layout_bottoni_colture = QHBoxLayout()
        self.layout_bottoni_colture.setSpacing(15)
        self.layout_card.addLayout(self.layout_bottoni_colture)

        self.label_messaggio = QLabel("")
        self.label_messaggio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_messaggio.setStyleSheet("font-size: 14px; font-weight: 500; border: none; background: transparent;")
        self.layout_card.addWidget(self.label_messaggio)
        self.layout_card.addSpacing(10)

        btn_annulla = QPushButton("Annulla e torna indietro")
        btn_annulla.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_annulla.setStyleSheet("""
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
        btn_annulla.clicked.connect(self.selezione_coltura)
        self.layout_card.addWidget(btn_annulla, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout_principale_schermata.addWidget(card_centrale)

        self.layout_bottoni_colture.addStretch(1)

        btn_personalizzato = QPushButton("Impostazioni\npersonalizzate")
        btn_fabbrica = QPushButton("Impostazioni\ndi fabbrica")
        btn_personalizzato.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_fabbrica.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_personalizzato.setFixedSize(140, 90)
        btn_fabbrica.setFixedSize(140, 90)

        stile_bottoni = """
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
            """
        btn_personalizzato.setStyleSheet(stile_bottoni)
        btn_fabbrica.setStyleSheet(stile_bottoni)

        btn_personalizzato.clicked.connect(lambda checked, p=pianta: self.inserimento_parametri_fenotipici(False, p))
        btn_fabbrica.clicked.connect(lambda checked, p=pianta: self.inserimento_parametri_fenotipici(True, p))

        self.layout_bottoni_colture.addWidget(btn_personalizzato)
        self.layout_bottoni_colture.addWidget(btn_fabbrica)
        self.layout_bottoni_colture.addStretch(1)

    def inserimento_parametri_fenotipici(self, fabbrica: bool, pianta: str):
        self.pianta_corrente = pianta
        self.fabbrica_corrente = fabbrica

        self.svuota_schermata()

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                font-family: '.AppleSystemUIFont', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                color: #FFFFFF;
            }
        """)

        card_centrale = QFrame()
        card_centrale.setFixedWidth(550)
        card_centrale.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
            }
        """)

        layout_card = QVBoxLayout(card_centrale)
        layout_card.setContentsMargins(50, 50, 50, 50)
        layout_card.setSpacing(25)

        titolo = QLabel("CARICARE DATI COLTURA")
        titolo.setStyleSheet(
            "font-size: 36px; font-weight: 700; letter-spacing: -0.5px; color: #FFFFFF; border: none; background: transparent;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_card.addWidget(titolo)

        sottotitolo1 = QLabel(f"Inserisci dati fenotipici per {pianta}")
        sottotitolo1.setStyleSheet(
            "font-size: 13px; color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
        sottotitolo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_card.addWidget(sottotitolo1)
        layout_card.addSpacing(15)

        # BUSTO
        layout_input1 = QVBoxLayout()
        label_id1 = QLabel("BUSTO PIANTE")
        label_id1.setStyleSheet(
            "font-size: 11px; font-weight: 700; letter-spacing: 1px; color: rgba(255, 255, 255, 0.4); border: none; background: transparent;")
        layout_input1.addWidget(label_id1)

        self.busto = QLineEdit()
        self.busto.setPlaceholderText("Inserisci larghezza busto piante in cm...")
        self.busto.setStyleSheet("""
            QLineEdit {
                        background-color: rgba(255, 255, 255, 0.06);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        border-radius: 12px;
                        padding: 14px 16px;
                        color: #FFFFFF;
                        font-size: 16px;
            }
            QLineEdit:focus {
                border: 1px solid #007AFF;
                background-color: rgba(255, 255, 255, 0.09);
            }
        """)
        layout_input1.addWidget(self.busto)
        layout_card.addLayout(layout_input1)

        # ALTEZZA
        layout_input2 = QVBoxLayout()
        label_id2 = QLabel("ALTEZZA PIANTE")
        label_id2.setStyleSheet(
            "font-size: 11px; font-weight: 700; letter-spacing: 1px; color: rgba(255, 255, 255, 0.4); border: none; background: transparent;")
        layout_input2.addWidget(label_id2)

        self.altezza = QLineEdit()
        self.altezza.setPlaceholderText("Inserisci altezza piante in cm...")
        self.altezza.setStyleSheet("""
                    QLineEdit {
                                background-color: rgba(255, 255, 255, 0.06);
                                border: 1px solid rgba(255, 255, 255, 0.1);
                                border-radius: 12px;
                                padding: 14px 16px;
                                color: #FFFFFF;
                                font-size: 16px;
                    }
                    QLineEdit:focus {
                        border: 1px solid #007AFF;
                        background-color: rgba(255, 255, 255, 0.09);
                    }
                """)
        layout_input2.addWidget(self.altezza)
        layout_card.addLayout(layout_input2)

        # AREA MESSAGGI DINAMICI
        self.label_messaggio = QLabel("")
        self.label_messaggio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_messaggio.setStyleSheet("font-size: 14px; font-weight: 500; border: none; background: transparent;")
        layout_card.addWidget(self.label_messaggio)

        layout_card.addSpacing(10)

        # Pulsanti annulla e salva
        layout_bottoni = QHBoxLayout()
        layout_bottoni.setSpacing(15)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_annulla.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 14px;
                font-size: 15px;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: #FFFFFF;
            }
        """)
        btn_annulla.clicked.connect(lambda checked, p=pianta: self.selezione_tipo_impostazioni(p))

        btn_salva = QPushButton("Registra i dati")
        btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_salva.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34C759, stop:1 #248A3D);
                border: none;
                border-radius: 12px;
                padding: 14px;
                font-size: 15px;
                font-weight: 600;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CD964, stop:1 #2CE256);
            }
            QPushButton:pressed {
                background: #1C6B30;
            }
        """)
        btn_salva.clicked.connect(self.gestisci_click_salva)

        layout_bottoni.addWidget(btn_annulla)
        layout_bottoni.addWidget(btn_salva)
        layout_card.addLayout(layout_bottoni)

        self.layout_principale_schermata.addWidget(card_centrale)

    def gestisci_click_salva(self):
        testo_altezza = self.altezza.text().strip()
        testo_busto = self.busto.text().strip()

        if not testo_altezza or not testo_busto:
            self.label_messaggio.setStyleSheet("color: #FF3B30; font-weight: 600; border: none; background: transparent;")
            self.label_messaggio.setText("Errore: Compila tutti i campi prima di salvare!")
            return

        try:
            float(testo_altezza.replace(',', '.'))
            float(testo_busto.replace(',', '.'))
        except ValueError:
            self.label_messaggio.setStyleSheet("color: #FF3B30; font-weight: 600; border: none; background: transparent;")
            self.label_messaggio.setText("Errore: Inserisci solo valori numerici!")
            return

        self.salva_dati_utente(self.pianta_corrente, testo_altezza, testo_busto, self.fabbrica_corrente)

    def conferma_selezione(self, pianta_scelta):
        self.label_messaggio.setStyleSheet("color: #34C759; font-weight: 600; border: none; background: transparent;")
        self.label_messaggio.setText(f"Impostata coltura: {pianta_scelta} sulla Serra")
        QTimer.singleShot(1500, self.torna_al_menu)

    def salva_dati_utente(self, pianta, altezza, busto, fabbrica):
        self.gestore_coltura.caricamento_dati_fenotipici(pianta, self.proprietario, busto, altezza, fabbrica)
        self.conferma_selezione(pianta)

    def torna_al_menu(self):
        if hasattr(self, 'label_messaggio') and self.label_messaggio:
            self.label_messaggio.setText("")
        self.proiettore_pagine.setCurrentIndex(0)

    # Quando lo stack visualizza questa schermata, aggiorna l'utente
    def showEvent(self, event):
        super().showEvent(event)

        # Recupero utente
        if self.proiettore_pagine.utente_corrente is not None:
            utente = self.proiettore_pagine.utente_corrente
            self.proprietario = getattr(utente, 'full_name', None) or getattr(utente, 'nome', None) or (utente[0] if isinstance(utente, (list, tuple)) and len(utente) > 0 else str(utente))

        self.selezione_coltura()
