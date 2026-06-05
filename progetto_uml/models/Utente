# definizione classe Utente con nome, cognome, email, password, ruolo assegnato (proprietario/operatore)
class Utente:
    def __init__(self, nome, cognome, email, password, ruolo=""):
        self.nome = nome.strip()
        self.cognome = cognome.strip()
        self.email = email.strip()
        self.password = password.strip()
        self.ruolo = ruolo.strip().lower()

    # restituisce una rappresentazione testuale dell'oggetto, utile per debug e stampa delle informazioni principali
    @property
    def full_name(self):
        if self.cognome:
            return f"{self.nome} {self.cognome}"
        return self.nome

    def __str__(self):
        return f"Utente(nome={self.full_name}, email={self.email}, ruolo={self.ruolo})"
