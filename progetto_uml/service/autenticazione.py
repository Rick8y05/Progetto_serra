from models.Utente import Utente


class Autenticazione:
    PROPRIETARIO = "proprietario"
    OPERATORE = "operatore"

    def __init__(self, utenti_repository):
        """
        INIZIALIZZAZIONE CLASSE AUTENTICAZIONE
        """
        self.repo = utenti_repository
        self.utente_corrente = None

    
    def login(self, email, password):
        """
        Metodo di login utente registrato con email e password 
        """
        email = email.strip()
        password = password.strip()


        for u in self.repo:
            if u["email"] == email and u["password"] == password:

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
        

        if "@" not in email:
            return False, "Email non valida"
        
        dominio = email.split("@")[-1]
        domini_validi = ["gmail.com", "outlook.com", "libero.it", "hotmail.com"]

        if dominio not in domini_validi:
            return False, "Dominio email non valido"

        if len(password) < 6:
            return False, "Password troppo corta (min. 6 caratteri)"

        speciali = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", "|", ";",
                    ":", ",", ".", "<", ">", "?"]
        
        if not any(c in speciali for c in password):
            return False, "Serve almeno un carattere speciale"


        for u in self.repo:
            if u["email"] == email:
                return False, "Utente già esistente"

        nuovo_utente = Utente(nome, cognome, email, password, self.PROPRIETARIO)


        self.repo.append({
            "nome": nuovo_utente.nome,
            "cognome": nuovo_utente.cognome,
            "email": nuovo_utente.email,
            "password": nuovo_utente.password,
            "ruolo": nuovo_utente.ruolo,
        })
        return True, "Registrazione completata"

   
    def get_utenti(self):
        """
        Getter utenti
        """
        return {u["email"]: u for u in self.repo}

    
    def logout(self):
        """
        Termine sessione
        """
        self.utente_corrente = None
