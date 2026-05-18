from repositories.dati_repository import DatiRepository

class Utente:
    utenti_registrati = {}

    # repository per il file utenti
    repo = DatiRepository("data/utenti.json", list)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def carica_utenti(cls):
        """Carica gli utenti dal repository in memoria"""
        dati = cls.repo.get_dati()

        if not isinstance(dati, list):
            dati = []

        cls.utenti_registrati = {
            u["email"]: u["password"]
            for u in dati
            if isinstance(u, dict) and "email" in u and "password" in u
        }

    @classmethod
    def salva_utenti(cls):
        """Salva gli utenti su file tramite repository"""
        dati = [
            {"email": email, "password": password}
            for email, password in cls.utenti_registrati.items()
        ]

        cls.repo.save(dati)

    def login(self):
        """Verifica credenziali"""
        return (
            self.email in Utente.utenti_registrati and
            Utente.utenti_registrati[self.email] == self.password
        )

    def logout(self):
        print("Logout effettuato")

    def registra(self):
        """Registra nuovo utente"""
        if self.email in Utente.utenti_registrati:
            return False

        if len(self.password) < 6:
            return False

        Utente.utenti_registrati[self.email] = self.password
        Utente.salva_utenti()
        return True

    def email_esiste(self):
        return self.email in Utente.utenti_registrati

    def password_usata(self):
        return self.password in Utente.utenti_registrati.values()


# inizializzazione automatica
Utente.carica_utenti()