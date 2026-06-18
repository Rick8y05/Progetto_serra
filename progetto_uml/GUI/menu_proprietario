from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt


class MenuProprietarioGUI(QWidget):

    def __init__(self, stack, auth, serra_service):
        super().__init__()

        self.stack = stack
        self.auth = auth
        self.serra_service = serra_service

        self.init_ui()

    def init_ui(self):

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: white;
                font-family: '.AppleSystemUIFont', 'SF Pro Display';
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---------------- CARD ----------------
        card = QFrame()
        card.setFixedWidth(650)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 24px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        # ---------------- WELCOME ----------------
        self.label_benvenuto = QLabel("")
        self.label_benvenuto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_benvenuto.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            background-color: #1E3A8A;
        """)
        card_layout.addWidget(self.label_benvenuto)

        # ---------------- TITOLO ----------------
        titolo = QLabel("MENU PROPRIETARIO")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 30px; font-weight: 700;")
        card_layout.addWidget(titolo)

        sottotitolo = QLabel("Gestione completa sistema serre")
        sottotitolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sottotitolo.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 13px;")
        card_layout.addWidget(sottotitolo)

        # ---------------- STATUS LABEL ----------------
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: #007AFF; font-size: 13px;")
        card_layout.addWidget(self.status)

        # ---------------- BUTTON FACTORY ----------------
        def crea_btn(testo, funzione):
            btn = QPushButton(testo)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.06);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 12px;
                    padding: 12px;
                    font-size: 15px;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.12);
                }
            """)
            btn.clicked.connect(funzione)
            return btn

        # ---------------- OPZIONI ----------------
        card_layout.addWidget(crea_btn("1 - Visualizza utenti", self.visualizza_utenti))
        card_layout.addWidget(crea_btn("2 - Visualizza serre", self.visualizza_serre))
        card_layout.addWidget(crea_btn("3 - Modalità funzionamento", self.modalita))
        card_layout.addWidget(crea_btn("4 - Controllo dispositivi", self.dispositivi))
        card_layout.addWidget(crea_btn("5 - Configura coltura", self.coltura))
        card_layout.addWidget(crea_btn("6 - Plancia dati", self.plancia))
        card_layout.addWidget(crea_btn("7 - Logout", self.logout))

        layout.addWidget(card)
        self.setLayout(layout)


    # ---------------- HEADER USER ----------------
    def mostra_utente(self):
        utente = self.stack.utente_corrente
        if utente:
            self.label_benvenuto.setText(f"Benvenuto, {utente.nome} (proprietario)")
        else:
            self.label_benvenuto.setText("Benvenuto")

    # ---------------- FEEDBACK UI ----------------
    def set_status(self, msg, color="#007AFF"):
        self.status.setText(msg)
        self.status.setStyleSheet(f"color: {color}; font-size: 13px;")

    # ---------------- FUNZIONI ----------------

    def visualizza_utenti(self):
        utenti = self.auth.get_utenti()
        self.set_status(f"Utenti: {len(utenti)}")

    def visualizza_serre(self):
        dati = self.serra_service.get_dati_plancia()
        self.set_status(f"Serre attive: {len(dati)}")

    def modalita(self):
        self.serra_service.set_modalita("automatica")
        self.set_status("Modalità impostata: automatica", "#34C759")

    def dispositivi(self):
        self.serra_service.azione_manuale("serra1", "1", "on")
        self.set_status("Dispositivo azionato", "#34C759")

    def coltura(self):
        self.set_status("Vai alla schermata coltura (da collegare)", "#FF9500")

    def plancia(self):
        dati = self.serra_service.get_dati_plancia()
        self.set_status(f"Dati plancia aggiornati ({len(dati)} serre)")

    def logout(self):
        self.auth.logout()
        self.stack.setCurrentIndex(0)

    def aggiorna_utente(self):
        utente = getattr(self.stack, "utente_corrente", None)

        if utente is None:
            self.label_benvenuto.setText("Benvenuto")
            return

        nome = getattr(utente, "nome", None)

        if not nome:
            nome = utente.email  # fallback utile

        self.label_benvenuto.setText(f"Benvenuto, {nome}")

    def visualizza_utenti(self):
        utenti = self.auth.get_utenti()

        print("\n=== UTENTI ===")
        for email, u in utenti.items():
            print(f"{email} - {u['ruolo']} - {u['nome']}")

    def visualizza_serre(self):
        dati = self.serra_service.get_dati_plancia()

        print("\n=== SERRA ===")
        for codice, info in dati.items():
            print(f"\nCodice: {codice}")
            print(f"Temperatura: {info.get('temperatura')}")
            print(f"Umidità: {info.get('umidita')}")
            print(f"Modalità: {info.get('modalita')}")
