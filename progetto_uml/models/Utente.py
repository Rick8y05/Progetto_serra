from repositories.dati_repository import DatiRepository

class Utente:
    utenti_registrati = {}

    # repository collegato al file utenti.json
    repo = DatiRepository("data/utenti.json", list)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def carica_utenti(cls):
        # Carica gli utenti dal file JSON tramite repository
        dati = cls.repo.get_dati

        cls.utenti_registrati = {
            utente["email"]: utente["password"]
            for utente in dati
            if isinstance(utente, dict) and "email" in utente and "password" in utente
        }

    @classmethod
    def salva_utenti(cls):
        # Salva gli utenti nel file JSON
        dati = [
            {
                "email": email,
                "password": password
            }
            for email, password in cls.utenti_registrati.items()
        ]
        cls.repo.save(dati)

    def login(self):
        # Verifica credenziali utente
        return (
            self.email in Utente.utenti_registrati
            and
            Utente.utenti_registrati[self.email] == self.password
        )

    # Logout utente
    def logout(self):
        print("Logout effettuato")

    # Registra un nuovo utente
    def registra(self):
        if self.email in Utente.utenti_registrati:
            print("Email già registrata")
            return False

        if len(self.password) < 6:
            print("Password troppo corta")
            return False

        Utente.utenti_registrati[self.email] = self.password
        Utente.salva_utenti()
        print("Registrazione completata")
        return True

    # Controlla se l'email inserita esiste già nel sistema
    def email_esiste(self):
        return self.email in Utente.utenti_registrati

    # Controlla se la password inserita è già stata utilizzata
    def password_usata(self):
        return self.password in Utente.utenti_registrati.values()

# caricamento automatico utenti all'avvio
Utente.carica_utenti()