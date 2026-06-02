from services.autenticazione import Autenticazione

class Menu:

    domini = ["gmail.com", "outlook.com", "libero.it", "hotmail.com"]
    caratteri_speciali = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",", ".", "<", ">", "/"]

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

    # login utente
    def accesso(self):
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        utente = self.auth.login(email, password)

        if utente:
            print(f"Login OK")
            print(f"Nome: {utente.nome}")
            print(f"Ruolo: {utente.ruolo}")
            return utente
        else: 
            print("Login fallito")
            return None
            

    # registrazione proprietario
    def registrazione(self):
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        password = input("Password (min 6): ").strip()

    # ---------------- PASSWORD ----------------
        if len(password) < 6:
            print("Password troppo corta")
            return

        ca_speciale = False
        for car in password:
            if car in self.caratteri_speciali:
                ca_speciale = True
                break

        if not ca_speciale:
            print("La password deve contenere almeno un carattere speciale!")
            return

    # ---------------- EMAIL ----------------
        if "@" not in email:
            print("Email non valida!")
            return

        dominio = email.split("@")[-1]

        dominio_valido = False
        for d in self.domini:
            if dominio == d:
                dominio_valido = True
                break

        if not dominio_valido:
            print("Email non valida!")
            return

    # ---------------- REGISTRAZIONE ----------------
        if self.auth.register_proprietario(nome, email, password):
            print("Registrazione OK")
        else:
            print("Utente già esistente")

    def esci(self):
        self.running = False
