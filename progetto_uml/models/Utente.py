class Utente:
    def __init__(self, email, password, ruolo):
        self.email = email.strip()
        self.password = password.strip()
        self.ruolo = ruolo.strip().lower()
        
    # rappresentazione utile per debug
    def __str__(self):
        return f"Utente(email={self.email}, ruolo={self.ruolo})"
