from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer

# configurazione parametri coltura
class SchermataConfiguraParametriColtura(QWidget):
    def __init__(self, proiettore_pagine, gestore_serra, gestore_coltura):
        super().__init__()
        self.proiettore_pagine = proiettore_pagine
        self.gestore_serra = gestore_serra
        self.proprietario = ""
        self.gestore_coltura = gestore_coltura
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
        titolo = QLabel("SELEZIONE PARAMETRI COLTURA")
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
        self.sottotitolo = QLabel("Seleziona la serra su cui intervenire")
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

        # bottone annulla
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

        self.selezione_serra()

    def svuota_layout_bottoni(self):
        """Svuota in modo sicuro e completo sia i widget che i relativi stretch/spaziatori dal layout orizzontale."""
        if self.layout_bottoni_colture is not None:
            while self.layout_bottoni_colture.count():
                item = self.layout_bottoni_colture.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    del item
    
    # schermata selezione serre
    def selezione_serra(self):
        self.svuota_layout_bottoni()
        self.sottotitolo.setText("Seleziona la serra su cui intervenire")

        # recupero serre utente
        n_univoci_proprietario = self.gestore_serra.parco_serre_proprietario(self.proprietario)

        # se non vi sono serre registrate per quel proprietario
        if not n_univoci_proprietario:
            label_vuota = QLabel("Non hai nessuna serra registrata nel tuo profilo.")
            label_vuota.setStyleSheet(
                "font-size: 14px; color: rgba(255, 255, 255, 0.4); font-style: italic; border: none; background: transparent;")
            self.layout_bottoni_colture.addWidget(label_vuota, alignment=Qt.AlignmentFlag.AlignCenter)
            return

        self.layout_bottoni_colture.addStretch(1)

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
            btn_serra.clicked.connect(lambda checked, id_scelto=n_univoco: self.selezione_coltura(id_scelto))
            self.layout_bottoni_colture.addWidget(btn_serra)

        self.layout_bottoni_colture.addStretch(1)

    # schermata selezione colture per serra
    def selezione_coltura(self, n_univoco):
        self.svuota_layout_bottoni()
        self.sottotitolo.setText(f"Scegli la coltura per la Serra {n_univoco}")

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

            btn_colture.clicked.connect(
                lambda _, p_scelta=pianta, serra_scelta=n_univoco: self.conferma_selezione(serra_scelta, p_scelta))
            self.layout_bottoni_colture.addWidget(btn_colture)

        self.layout_bottoni_colture.addStretch(1)

    # conferma modifica coltura serra
    def conferma_selezione(self, id_serra, pianta_scelta):
        self.gestore_serra.modifica_coltura_serra(id_serra, pianta_scelta)
        self.label_messaggio.setStyleSheet("color: #34C759; font-weight: 600; border: none; background: transparent;")
        self.label_messaggio.setText(f" Impostata coltura: {pianta_scelta} sulla Serra {id_serra}")

        QTimer.singleShot(1500, self.torna_al_menu)

    def torna_al_menu(self):
        self.label_messaggio.setText("")
        self.proiettore_pagine.setCurrentIndex(0)

    def showEvent(self, event):
        super().showEvent(event)

        if self.proiettore_pagine.utente_corrente is not None:
            utente = self.proiettore_pagine.utente_corrente
            if hasattr(utente, 'full_name'):
                self.proprietario = utente.full_name
            elif hasattr(utente, 'nome') and hasattr(utente, 'cognome'):
                self.proprietario = f"{utente.nome} {utente.cognome}".strip()
            else:
                self.proprietario = utente[0] if isinstance(utente, (list, tuple)) and len(utente) > 0 else str(utente)

        if hasattr(self, 'label_messaggio') and self.label_messaggio:
            self.label_messaggio.setText("")

        self.selezione_serra()
