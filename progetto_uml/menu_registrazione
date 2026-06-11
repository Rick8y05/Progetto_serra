from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt6.QtCore import Qt

# schermata di registrazione utenti (permette la creazione di un nuovo proprietario nel sistema)
class SchermataRegistrazione(QWidget):

    def __init__(self, stack, auth):
        super().__init__()
        self.stack = stack
        self.auth = auth
        self.init_ui()

    # costruzione interfaccia grafica
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(450)

        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.04);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel {
                color: #FFFFFF;
                border: none;
                background: transparent;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.06); 
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px; 
                padding: 12px; 
                color: #FFFFFF;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 12px;
                color: #FFFFFF;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)

        # titolo schermata
        titolo = QLabel("REGISTRAZIONE")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 26px; font-weight: 700; background: transparent;")
        card_layout.addWidget(titolo)

        # input per inserimento nome
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome")

        # input per inserimento cognome
        self.cognome = QLineEdit()
        self.cognome.setPlaceholderText("Cognome")

        # input per inserimento email
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        # input per inserimento password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.msg = QLabel("")
        self.msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg.setStyleSheet("color: #FF3B30; font-weight: 600; font-size: 14px;")

        # pulsanti
        btn_reg = QPushButton("Registra")
        btn_back = QPushButton("Indietro")

        btn_reg.clicked.connect(self.registra)
        btn_back.clicked.connect(self.torna_indietro)

        card_layout.addWidget(self.nome)
        card_layout.addWidget(self.cognome)
        card_layout.addWidget(self.email)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.msg)
        card_layout.addWidget(btn_reg)
        card_layout.addWidget(btn_back)

        layout.addWidget(card)
        self.setLayout(layout)

    # logica registrazione utente
    def registra(self):
        # registrazione con nome, cognome, email e password
        ok, messaggio = self.auth.register_proprietario(
            self.nome.text(), 
            self.cognome.text(), 
            self.email.text(), 
            self.password.text()
        )

        # se la registrazione va a buon fine
        if ok:
            # Svuota i campi così al prossimo accesso la schermata è pulita
            self.nome.clear()
            self.cognome.clear()
            self.email.clear()
            self.password.clear()
            self.msg.setText("")

            # Torna al login
            self.stack.setCurrentIndex(11)

        else:
            self.msg.setText(messaggio)

    def torna_indietro(self):
        # Quando l'utente clicca "Indietro", la schermata viene ripulita da vecchi testi o errori
        self.nome.clear()
        self.cognome.clear()
        self.email.clear()
        self.password.clear()
        self.msg.setText("")
        self.stack.setCurrentIndex(11)
