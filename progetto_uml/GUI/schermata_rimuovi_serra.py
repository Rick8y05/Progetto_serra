from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer

# rimozione serra
class SchermataRimuoviSerra(QWidget):
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
        titolo = QLabel("RIMUOVI SERRA")
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
        sottotitolo = QLabel("Seleziona la serra che desideri rimuovere dal tuo parco serre")
        sottotitolo.setStyleSheet(
            "font-size: 18px; color: rgba(255, 255, 255, 0.5); border: none; background: transparent;")
        sottotitolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_card.addWidget(sottotitolo)

        self.layout_card.addSpacing(10)

        self.layout_bottoni_serre = QHBoxLayout()
        self.layout_bottoni_serre.setSpacing(15)
        self.layout_card.addLayout(self.layout_bottoni_serre)

        self.label_messaggio = QLabel("")
        self.label_messaggio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_messaggio.setStyleSheet("font-size: 14px; font-weight: 500; border: none; background: transparent;")
        self.layout_card.addWidget(self.label_messaggio)
        self.layout_card.addSpacing(10)
        
        # bottone annulla e torna al menu
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

        layout_principale.addWidget(card_centrale)
        self.setLayout(layout_principale)


    def aggiorna_pulsanti_serre(self):
        if self.layout_bottoni_serre is not None:
            while self.layout_bottoni_serre.count():
                item = self.layout_bottoni_serre.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                del item  

        n_univoci_proprietario = self.gestore_serra.parco_serre_proprietario(self.proprietario)

        # se non vengono trovate serre registrate
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
                    background-color: rgba(255, 37, 37, 0.15);
                    border-color: #FF3B30;
                }
            """)

            btn_serra.clicked.connect(lambda checked, id_scelto=n_univoco: self.conferma_rimozione(id_scelto))
            self.layout_bottoni_serre.addWidget(btn_serra)

        self.layout_bottoni_serre.addStretch(1)
    
    def conferma_rimozione(self, id_scelto):
        successo, messaggio = self.gestore_serra.rimuovi_serra(id_scelto, self.proprietario)

        if successo:
            self.label_messaggio.setStyleSheet(
                "color: #34C759; font-weight: 600; border: none; background: transparent;")
            self.label_messaggio.setText(f" {messaggio}")

            self.notifica_modifica_parco_serre()

            self.aggiorna_pulsanti_serre()
            QTimer.singleShot(1200, self.torna_al_menu)
        else:
            self.label_messaggio.setStyleSheet(
                "color: #FF3B30; font-weight: 600; border: none; background: transparent;")
            self.label_messaggio.setText(f"✕ {messaggio}")

    def notifica_modifica_parco_serre(self):
        for i in range(self.proiettore_pagine.count()):
            widget_corrente = self.proiettore_pagine.widget(i)
            if widget_corrente != self:
                if hasattr(widget_corrente, 'aggiorna_pulsanti_serre'):
                    widget_corrente.aggiorna_pulsanti_serre()
                elif hasattr(widget_corrente, 'aggiorna_lista_serre'):
                    widget_corrente.aggiorna_lista_serre()

    def torna_al_menu(self):
        self.label_messaggio.setText("")
        self.proiettore_pagine.setCurrentIndex(0)

    def showEvent(self, event):
        super().showEvent(event)

        if self.proiettore_pagine.utente_corrente is not None:
            utente = self.proiettore_pagine.utente_corrente
            self.proprietario = utente.nome if hasattr(utente, 'nome') else utente[0]

        self.aggiorna_pulsanti_serre()
