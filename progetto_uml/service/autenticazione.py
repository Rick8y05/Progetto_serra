from repository.utenti_repository import UtentiRepository
from models.Utente import Utente


class Autenticazione:

    PROPRIETARIO = "proprietario"
    OPERATORE = "operatore"

    def __init__(self):
        self.repo = UtentiRepository()
        self.utente_corrente = None

    # login utente
    def login(self, email, password):
        email = email.strip()
        password = password.strip()

        utenti = self.repo.get_all()

        for u in utenti:
            if u["email"] == email and u["password"] == password:
                return Utente(u["email"], u["password"], u["ruolo"])

        return None

    # registrazione proprietario
    def register_proprietario(self, email, password):
        email = email.strip()
        password = password.strip()

        utenti = self.repo.get_all()

        for u in utenti:
            if u["email"] == email:
                return False

        utenti.append({
            "email": email,
            "password": password,
            "ruolo": self.PROPRIETARIO
        })

        self.repo.save_all(utenti)
        return True

    # utenti
    def get_utenti(self):
        utenti = self.repo.get_all()
        return {u["email"]: u for u in utenti}

    def logout(self):
        self.utente_corrente = None