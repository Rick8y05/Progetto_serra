from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer

# schermata per aggiungere una serra
class SchermataAggiungiSerra(QWidget):
    def __init__(self, proiettore_pagine, gestore_serra):
        super().__init__()
        self.proiettore_pagine = proiettore_pagine
        self.gestore_serra = gestore_serra
        self.proprietario = ""
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
        layout_principale.setContentsMargins(0, 0, 0, 0)

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

        # titolo schermata
        titolo = QLabel("Nuova Serra")
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
        layout_card.addWidget(titolo)

        # sottotitolo schermata
        sottotitolo = QLabel("Registra una nuova serra nel sistema.")
        sottotitolo.setStyleSheet(
            "font-size: 13px; color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
        sottotitolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_card.addWidget(sottotitolo)
        layout_card.addSpacing(15)

        # input numero univoco serre
        layout_input = QVBoxLayout()
        label_id = QLabel("NUMERO UNIVOCO SERRE")
        label_id.setStyleSheet("""
            QLabel {
                        font-size: 11px; 
                        font-weight: 700; 
                        letter-spacing: 1px; 
                        color: rgba(255, 255, 255, 0.4);
                        border: none;
                        background: transparent;
            }
        """)
        layout_input.addWidget(label_id)

        self.n_univoco = QLineEdit()
        self.n_univoco.setPlaceholderText("Inserisci il numero univoco...")
        self.n_univoco.setStyleSheet("""
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
        layout_input.addWidget(self.n_univoco)
        layout_card.addLayout(layout_input)

        self.label_messaggio = QLabel("")
        self.label_messaggio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_messaggio.setStyleSheet("font-size: 14px; font-weight: 500; border: none; background: transparent;")
        layout_card.addWidget(self.label_messaggio)

        layout_card.addSpacing(10)

        layout_bottoni = QHBoxLayout()
        layout_bottoni.setSpacing(15)

        # pulsante annulla
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
        btn_annulla.clicked.connect(self.torna_al_menu)

        # bottone salva
        btn_salva = QPushButton("Registra Serra")
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
        btn_salva.clicked.connect(self.salva_serra_nella_logica)

        layout_bottoni.addWidget(btn_annulla)
        layout_bottoni.addWidget(btn_salva)
        layout_card.addLayout(layout_bottoni)

        layout_principale.addWidget(card_centrale)
        self.setLayout(layout_principale)

    def torna_al_menu(self):
        self.n_univoco.clear()
        self.label_messaggio.setText("")
        self.proiettore_pagine.setCurrentIndex(0)

    def salva_serra_nella_logica(self):
        n_univoco = self.n_univoco.text().strip()

        # controllo validità del numero univoco
        if n_univoco == "":
            self.label_messaggio.setStyleSheet("color: #FF3B30; font-weight: 600; background: transparent;")
            self.label_messaggio.setText("Inserisci un numero univoco della serra valido.")
            return  # return per evitare di continuare se vuoto

        successo, messaggio = self.gestore_serra.aggiungi_serra(n_univoco, self.proprietario)

        if successo:
            self.label_messaggio.setStyleSheet("color: #34C759; font-weight: 600; background: transparent;")
            self.label_messaggio.setText(f" {messaggio}")

            # aggiornamento dizionari schermate coinvolte
            for i in range(self.proiettore_pagine.count()):
                widget_corrente = self.proiettore_pagine.widget(i)

                if hasattr(widget_corrente, 'aggiorna_pulsanti_serre'):
                    widget_corrente.aggiorna_pulsanti_serre()
                elif hasattr(widget_corrente, 'aggiorna_lista_serre'):
                    widget_corrente.aggiorna_lista_serre()
            # ritorno al menu dopo 1.2 secondi
            QTimer.singleShot(1200, self.torna_al_menu)
        else:
            self.label_messaggio.setStyleSheet("color: #FF3B30; font-weight: 600; background: transparent;")
            self.label_messaggio.setText(f" {messaggio}")

    def showEvent(self, event):
        super().showEvent(event)

        if self.proiettore_pagine.utente_corrente is not None:
            utente = self.proiettore_pagine.utente_corrente
            self.proprietario = getattr(utente, "nome", None)
        else:
            self.proprietario = None
