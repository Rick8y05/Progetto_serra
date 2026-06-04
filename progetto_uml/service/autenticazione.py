from repository.utenti_repository import UtentiRepository
from models.Utente import Utente

from repository.utenti_repository import UtentiRepository
from models.Utente import Utente

from repository.utenti_repository import UtentiRepository
from models.Utente import Utente

# classe che gestisce l'autenticazione degli utenti
class Autenticazione:
    # ruoli possibili
    PROPRIETARIO = "proprietario"
    OPERATORE = "operatore"

    def __init__(self):
        self.repo = UtentiRepository()
        self.utente_corrente = None

    # login utente registrato con email e password (verificate nel file utenti.json)
    def login(self, email, password):
        email = email.strip()
        password = password.strip()

        utenti = self.repo.get_all()

        # scorre lista utenti fino a trovare un eventuale corrispondenza di email e password con email e password già registrate
        for u in utenti:
            if u["email"] == email and u["password"] == password:
                # crea un nuovo oggetto Utente 
                return Utente(u["nome"], u["email"], u["password"], u["ruolo"], )

        return None

    # registrazione di un nuovo proprietario
    def register_proprietario(self, nome, email, password):
        email = email.strip()
        password = password.strip()

        utenti = self.repo.get_all()

        # controlla se l'email è già stata registrata
        for u in utenti:
            if u["email"] == email:
                return False

        # aggiunge il nuovo prorietario alla lista utenti
        utenti.append({
            "nome": nome,
            "email": email,
            "password": password,
            "ruolo": self.PROPRIETARIO
        })

        # salva la lista utenti aggiornata nel file json
        self.repo.save_all(utenti)
        return True

    # utenti
    def get_utenti(self):
        utenti = self.repo.get_all()
        return {u["email"]: u for u in utenti}

    # termine sessione
    def logout(self):
        self.utente_corrente = None
