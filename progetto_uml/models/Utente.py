
class Utente:
    """
    Rappresenta un utente del sistema
    """
    def __init__(self, nome, cognome, email, password, ruolo=""):
        """
        Inizializzazione utente
        """
        self.nome = nome.strip()
        self.cognome = cognome.strip()
        self.email = email.strip()
        self.password = password.strip()
        self.ruolo = ruolo.strip().lower()

    
    @property
    def full_name(self):
        if self.cognome:
            return f"{self.nome} {self.cognome}"
        return self.nome

    def __str__(self):
        return f"Utente(nome={self.full_name}, email={self.email}, ruolo={self.ruolo})"
