from repository.utenti_repository import UtentiRepository
from models.Utente import Utente

# classe che gestisce l'autenticazione degli utenti
class Autenticazione:
    # ruoli possibili
    PROPRIETARIO = "proprietario"
    OPERATORE = "operatore"

    def __init__(self):
        """
        INIZIALIZZAZIONE CLASSE AUTENTICAZIONE
        """
        self.repo = UtentiRepository()
        self.utente_corrente = None

    
    def login(self, email, password):
        """
        Metodo di login utente registrato con email e password 
        """
        email = email.strip()
        password = password.strip()

        utenti = self.repo.get_all()

        # scorre lista utenti fino a trovare un eventuale corrispondenza di email e password con email e password già registrate
        for u in utenti:
            if u["email"] == email and u["password"] == password:
                # crea un nuovo oggetto Utente, supportando anche il cognome
                return Utente(u["nome"], u.get("cognome", ""), u["email"], u["password"], u["ruolo"])
        return None

   
    def register_proprietario(self, nome, cognome, email, password):
        """
        Metodo di registrazione di un nuovo proprietario
        """
        nome = nome.strip()
        cognome = cognome.strip()
        email = email.strip()
        password = password.strip()

        if not nome or not cognome or not email or not password:
            return False, "Compila tutti i campi"
        
        # controllo email
        if "@" not in email:
            return False, "Email non valida"
        
        dominio = email.split("@")[-1]
        domini_validi = ["gmail.com", "outlook.com", "libero.it", "hotmail.com"]

        if dominio not in domini_validi:
            return False, "Dominio email non valido"
        
        # controllo password
        if len(password) < 6:
            return False, "Password troppo corta (min. 6 caratteri)"
        
        
        speciali = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", "|", ";",
                    ":", ",", ".", "<", ">", "?"]
        
        if not any(c in speciali for c in password):
            return False, "Serve almeno un carattere speciale"

        utenti = self.repo.get_all()

        # controlla se l'email è già stata registrata
        for u in utenti:
            if u["email"] == email:
                return False, "Utente già esistente"

        nuovo_utente = Utente(nome, cognome, email, password, self.PROPRIETARIO)

        # aggiunge il nuovo prorietario alla lista utenti
        utenti.append({
            "nome": nuovo_utente.nome,
            "cognome": nuovo_utente.cognome,
            "email": nuovo_utente.email,
            "password": nuovo_utente.password,
            "ruolo": nuovo_utente.ruolo,
        })

        # salva la lista utenti aggiornata nel file json
        self.repo.save_all(utenti)
        return True, "Registrazione completata"

   
    def get_utenti(self):
        """
        Getter utenti
        """
        utenti = self.repo.get_all()
        return {u["email"]: u for u in utenti}

    
    def logout(self):
        """
        Termine sessione
        """
        self.utente_corrente = None
