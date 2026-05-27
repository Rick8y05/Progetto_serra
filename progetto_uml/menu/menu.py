from services.autenticazione import Autenticazione

class Menu:

    def __init__(self):
        self.auth = Autenticazione()
        self.running = True

    def mostra_menu(self):
        print("\n=== MENU PRINCIPALE ===")
        print("1 - Login")
        print("2 - Registra proprietario")
        print("3 - Esci")

    def scegli_opzione(self):
        return input("> ")

    # ---------------- LOGIN ----------------
    def accesso(self):
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        utente = self.auth.login(email, password)

        if utente:
            print(f"Login OK -> {utente.ruolo}")
            return utente
        else:
            print("Login fallito")
            return None

    # ---------------- REGISTRAZIONE ----------------
    def registrazione(self):
        email = input("Email: ")
        password = input("Password (min 6): ")

        if len(password) < 6:
            print("Password troppo corta")
            return

        if self.auth.register_proprietario(email, password):
            print("Registrazione OK")
        else:
            print("Utente già esistente")

    def esci(self):
        self.running = False
